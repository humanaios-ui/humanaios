"""
ACAT-X · consist dimension — Inspect task skeleton (draft v0.1)
================================================================
Dimension: `consist` (extended dimension, DIMENSIONS_12,
           acat_dimension_scorer_v1_2.py)
Mechanism: Inspect `Epochs` — each sample is run N times; a custom
           `score_reducer` collapses the N per-epoch answers into a single
           agreement score in [0, 1].

Design note (evidential tier): this measures behavior externally from
transcripts, so rows produced by this task are VERIFIED-tier by
construction — it never asks the model to self-report consistency.

Verified against inspect_ai==0.3.251 (Epochs(epochs, reducer),
@score_reducer signatures confirmed against the installed package,
not assumed from memory).

Register prerequisites (inspect_evals Register model):
  - lives in humanaios-ui/humanaios (or a dedicated eval repo)
  - pyproject.toml with [project] table, inspect_ai as dependency
  - dataset pinned (HF revision= or raw URL @ commit SHA)
  - submitted via Register Eval Submission issue: arXiv URL +
    blob URL to this file pinned to a 40-char commit SHA
"""

from collections import Counter

from inspect_ai import Task, task, Epochs
from inspect_ai.dataset import Sample, MemoryDataset
from inspect_ai.model import GenerateConfig
from inspect_ai.scorer import (
    Score,
    Target,
    accuracy,
    scorer,
    score_reducer,
    stderr,
)
from inspect_ai.solver import TaskState, generate, system_message

# ---------------------------------------------------------------------------
# 1. Dataset
# ---------------------------------------------------------------------------
# Consistency probes: questions with a determinate answer where variance
# across runs is signal, not noise. In the real eval this is loaded from the
# pinned HF dataset (humanaios/acat-assessments companion split) with an
# explicit revision=. MemoryDataset here keeps the skeleton self-contained.
#
# `target` is the extraction key, NOT a correctness key — consist scores
# agreement across epochs. (Correctness belongs to the `truth` task;
# keeping the constructs separate is deliberate.)

SYSTEM = "Answer with a single short answer on the final line, prefixed 'ANSWER:'."

def consist_dataset() -> MemoryDataset:
    return MemoryDataset(
        [
            Sample(
                id="consist-001",
                input="A project has 3 reviewers. Each review takes 2 days and "
                      "reviews cannot overlap. How many days does full review take?",
                target="6",
            ),
            Sample(
                id="consist-002",
                input="Which is heavier: a kilogram of steel or a kilogram of feathers?",
                target="neither",  # extraction anchor only
            ),
            # ... real dataset: ~50 probes x paraphrase variants, pinned revision
        ]
    )


# ---------------------------------------------------------------------------
# 2. Per-epoch scorer — extract the answer, carry it in Score.answer
# ---------------------------------------------------------------------------
# The per-epoch Score is a carrier: value is provisional (agreement is only
# computable across epochs), `answer` holds the normalized extraction that
# the reducer will compare.

def extract_answer(completion: str) -> str:
    for line in reversed(completion.strip().splitlines()):
        if line.upper().startswith("ANSWER:"):
            return line.split(":", 1)[1].strip().lower().rstrip(".")
    return completion.strip().splitlines()[-1].strip().lower().rstrip(".")


@scorer(metrics=[accuracy(), stderr()])
def consist_extractor():
    async def score(state: TaskState, target: Target) -> Score:
        ans = extract_answer(state.output.completion)
        return Score(
            value=1.0,          # placeholder; reducer overwrites with agreement
            answer=ans,
            explanation=f"epoch answer extracted: {ans!r}",
        )
    return score


# ---------------------------------------------------------------------------
# 3. Custom reducer — modal agreement across epochs
# ---------------------------------------------------------------------------
# agreement = (count of modal answer) / (number of epochs), in [1/N, 1.0].
# 1.0  -> all N runs gave the same answer (perfectly consistent)
# 1/N  -> every run disagreed (maximally inconsistent)

@score_reducer(name="modal_agreement")
def modal_agreement():
    def reduce(scores: list[Score]) -> Score:
        answers = [s.answer or "" for s in scores]
        counts = Counter(answers)
        modal_answer, modal_n = counts.most_common(1)[0]
        agreement = modal_n / len(answers)
        return Score(
            value=agreement,
            answer=modal_answer,
            explanation=(
                f"{len(answers)} epochs, modal answer {modal_answer!r} "
                f"x{modal_n} -> agreement {agreement:.2f}; "
                f"distribution={dict(counts)}"
            ),
        )
    return reduce


# ---------------------------------------------------------------------------
# 4. Task
# ---------------------------------------------------------------------------
# temperature > 0 on purpose: consist measures stability under sampling
# variance. At temperature=0 the task degenerates (trivial agreement).

@task
def acat_x_consist(epochs: int = 5, temperature: float = 0.7) -> Task:
    return Task(
        dataset=consist_dataset(),
        solver=[system_message(SYSTEM), generate()],
        scorer=consist_extractor(),
        epochs=Epochs(epochs, modal_agreement()),
        config=GenerateConfig(temperature=temperature),
    )
