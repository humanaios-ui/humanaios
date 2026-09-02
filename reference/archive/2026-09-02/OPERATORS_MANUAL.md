# Z2 ledger — operator's manual
Version 1.7 · plain words · this text is built into the app — tap **? how** top right on any screen and it opens at the section for that screen; tap the title for the whole thing and also ships as OPERATORS_MANUAL.md

## 1. What this is

One file. It runs in your phone's browser with no internet and no account. It holds every decision the project is waiting on you for, and it writes each decision you make into a chain of records that can't be quietly changed. You work the chain; Claude (Z1) reads it when you paste it; the project moves.

Three things to hold in mind:

- **A tick is a claim.** When you mark something done, the ledger records that *you said so*. It doesn't check.
- **A matching hash is verification.** When you paste the fingerprint of a file and it matches the one on record, the ledger marks it verified. That is the only thing it checks for you.
- **The export is the receipt.** The phone saves as you go, but phones lose things. The JSON you export is the record. Export at every close.

## 2. Words used

- **Ruling** — a question with two or more readings, waiting for you to pick one. Every option is a full answer; none is Claude's preference.
- **Input** — something only you can supply: a credential, a batch of real data, an application you file. No ruling substitutes for it.
- **File** — a staged artifact and the one move you make on it: *land* it to the repository, *run* it, *ratify* its hash, *read* it, give it a *tone pass*, or just *use* it.
- **Window** — a date after which a move stops being possible.
- **Hash / pin / sha256** — a 64-character fingerprint of a file. If one character of the file changes, the fingerprint changes completely. Pinning a hash means writing that fingerprint down so the file can be checked later.
- **Chain** — the list of everything you've done in this ledger. Each record carries the fingerprint of the record before it, so nothing can be inserted, removed or edited without the chain breaking. The rail at the top shows the chain count and turns red if it breaks.
- **Chain head** — the fingerprint of the newest record. Quoting it in a message pins exactly which state of the ledger you're talking about.
- **Seed** — the starting set of items the ledger was built with. Everything after that is a record on the chain.
- **Patch** — a small file Claude sends back that adds or edits items. Import it, or, when Claude bundles patches inside a new version of this file, tap *Apply all* on the banner; either way the changes land as records tagged *Z1*, and a patch already on your chain is skipped. A patch can never rule, claim, verify or ratify — only you can.
- **Evidence** — a link (PR, commit, file) and a note attached to a claim. It is a pointer for Claude to fetch, not proof; only a matching sha is proof.
- **Handoff** — the paste block from the Session screen. It's how the chain reaches Claude. Pasting it *is* the ratification of what it lists.
- **Session** — one sitting. Open it, work, close it. Numbers go S1, S2, S3 so both sides can refer to the same sitting.

## 3. The five screens

**Next** — one item at a time, most urgent first. The big green buttons at the bottom are the decision. Below the card: "up next" so you can see what's coming. *Skip for now* sends an item to the back. *Ask Z1* opens a box for a question about this exact item (§5). Deadlines inside three days show red; inside fourteen, amber.

**Rulings** — the full list. Rule inline, or tap › to bring one into Next. Ruled rows dim; they stay so the export shows them. "Accept FALS-43 batch" is one tap because that ruling is 43 identical decisions.

**Files** — every staged artifact grouped by what you do with it. Expand a card for its command (copy button), its pin, and a box to paste a fingerprint for verification. The filter row narrows to *to land*, *to run*, and so on.

**Ledger** — what we've learned (principles that earned a line), the chain itself (every record, filterable), and *Grow it* — forms to add a ruling, file, input, window, artifact, learning or note by hand. Retire never deletes; it dims the item out of the queue and leaves the record.

**Session** — open and close the sitting; inputs; windows; ratify by hash; the handoff block; one-tap callouts to Claude; close checklist; export, import, theme, reset.

## 4. A sitting, start to finish

1. Open the file. Tap **Session → Open session**. Tick the three open steps — the first one (fetch the live registry and pin its sha) is the only one that matters if you skip the others.
2. Go to **Next**. Rule, deliver or claim until the queue is clear or you're done for the day. Undo is the banner that appears for eight seconds after each decision. Undo is itself a record; nothing is erased.
3. Anything you land: when you tap *Landed*, a box offers to attach the PR or commit link and a note — do it, it saves Claude a search. Then verify: expand the card, paste the output of `sha256sum <file>`, watch the status line say *verified*. Three tiers: CLAIM (your word), CLAIM+LINK (your word plus a pointer Claude can fetch), VERIFIED (the sha matched).
4. **Session → Ratify by hash**: tick the artifacts you're ratifying. A ruling that says "ratify" is intent; this tick is the act.
5. **Copy handoff block**. Paste it to Claude. Then **Mark handed off** so the next block only carries what's new.
6. Tick the close steps, **Close session**, **Export**. Put the JSON somewhere that isn't the phone.

Five minutes is enough for steps 1, 5 and 6 on a day with no decisions.

## 5. Asking for help from inside the ledger

Every item is a claim about the cheapest path known when it was written. Paths change — the credential item turned from "issue a PAT" into three options after one exchange. When an item looks wrong, thin, or you don't know how to do it:

1. On the item's card in **Next**, tap **Ask Z1**. Write the question in plain words. *Record and copy*.
2. Paste the copied block to Claude. It carries the item, its current text, the chain head and your question.
3. Claude answers with a **patch**. Import it on the Ledger screen. The card then shows a one-line **Z1 answered** box first, then **directions** (steps), **what we learned** (the principle), and a **source** link. The "asked Z1" line clears when the answer lands, not when you hand off. Until the patch is imported the card can't know an answer exists — the chain only holds what's on the device.

The handoff block lists open asks too, so a question you asked on Tuesday reaches Claude on Thursday even if you forgot.

## 6. What the phone keeps, and what it doesn't

The browser saves every change on the device (the "saved hh:mm" stamp top right). This survives closing the tab. It does not survive clearing browser data, a browser reinstall, or in some browsers a long time unopened. Treat it as a convenience.

The export JSON contains the whole chain plus a readable snapshot. Import it on any device: if that device is empty, it takes the chain whole; if it already has records, you choose *merge* (both sets, the merge itself recorded) or *replace*.

**Reset this device** erases the local chain. There is no undo for it. Export first.

## 7. When something looks wrong

- **Rail's chain block is red / "chain BROKEN at seq N"** — a record was altered or the storage got corrupted. Stop working on it. Export what's there, paste the export to Claude, and restore from your last good export. A broken chain is evidence, not a bug to work around.
- **Counts on the rail don't match what you remember** — check the Ledger screen's chain list; every change is there with a time. If something is missing, it was never recorded, which means the tap didn't take or the save failed.
- **"not saving — export"** in the top right — the browser refused storage. Everything still works this sitting; export before closing or it's gone.
- **Import says "not a recognised export"** — the file isn't from this app or a patch in the documented shape. Send it to Claude rather than editing it.
- **An item is wrong** — edit it (the *edit* link on any card) or ask Z1. Don't delete; retire.

## 8. How this grows

The rule that keeps it honest: **the chain format and the seed fingerprint never change.** Screens, buttons, colours, the device it runs on — all of that is the projection and can change freely. What a record *is* — sequence, time, type, reference, value, who, previous hash, own hash — is fixed. Any future version must replay today's chain and get the same picture. If it can't, it isn't a version of this ledger.

**Stage 1 — phone (now).** One file, one thumb, one queue. Items grow by patch and by the forms. Nothing to install.

**Stage 2 — desktop (already works).** Open the same file on a wide screen: navigation moves to the left, the queue list appears beside the card, keys 1–3 rule, `s` skips, `u` undoes. Carry the chain across by export/import. Trigger to make desktop the primary: the day most landing happens from a terminal rather than a phone — that's when a wide screen next to the terminal beats a phone in the other hand.

**Stage 3 — browser extension (proposed, not built).** Same code, packaged so the browser treats it as an app. Three things it adds that a plain file cannot: storage that survives cache clears; a badge on the toolbar with the open count; and, the real reason to do it, reading GitHub pages you're already looking at — so when you open a pull request or a file on main, the extension can compare its sha to the pin on your ledger and mark it *verified on main* without you pasting anything. That is the IC-030 live read done by code instead of memory. Costs: a manifest, a store review or side-load, and a second place the chain lives. Trigger: when verification by paste becomes the slowest step of a sitting, or when the second operator arrives. Prior that it's worth building before either trigger: 0.2.

**Stage 4 — hosted, two operators (not proposed yet).** Only if a second Z2 exists. Then the chain needs a server or a shared repository as its home, merges become routine, and the "only you can rule" property needs real identity behind it. Nothing in the format has to change; the trust model does. Don't build ahead of the second person.

**What must not happen at any stage:** a version that can rule, claim or ratify on your behalf; a version that edits a record instead of appending one; a patch type that lets Z1 do either. If a proposed feature needs one of those, the feature is wrong.

## 9. Ten-second card

Open session → work Next → verify what you landed → tick ratifications → copy handoff → paste to Claude → mark handed off → close → export. Ask Z1 from any card. The tick is your word; the hash is the proof; the export is the receipt.
