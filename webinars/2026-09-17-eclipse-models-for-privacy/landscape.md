# The Agent Identity Landscape · September 2026

Backup notes for the "Landscape" slide of the Eclipse Models for Privacy webinar (2026-09-17). One section per table row: what it is, pros, cons, and how it relates to Verana. Evaluation axis = the deck's rubric: **who it is / who operates it / what it may do / no central observer**.

---

## 1. Enterprise agent IAM

**Examples.** Microsoft Entra Agent ID (GA spring 2026, part of Agent 365), Okta for AI Agents (GA April 30, 2026, integrates AWS Bedrock AgentCore), AWS AgentCore Identity, Cross App Access (XAA) semantics added to the MCP spec (November 2025 revision).

**What it is.** The enterprise identity stack (IAM) extended to non-human identities: each AI agent gets a directory identity in the tenant, with lifecycle management, conditional access, least privilege, monitoring, and integration into the Zero Trust tooling the company already runs.

**Pros.**
- Mature, operational today, backed by the vendors enterprises already trust and pay.
- Real lifecycle governance: provisioning, deprovisioning, access reviews, anomaly detection.
- Deep integration with existing policy engines (Conditional Access, Purview, workload identity federation).
- The right tool for the intra-company problem: which of OUR agents may touch WHICH of our systems.

**Cons.**
- Tenant-scoped by design: identity and trust stop at the organization boundary. Cross-org trust is bilateral admin configuration inside the vendor's hub.
- The platform is the observer: the hub sees every authentication and can correlate all activity.
- No public verifiability: an outside counterparty cannot check anything, and nothing binds the agent to a legal entity in a way a stranger can verify.
- No accreditation semantics: internal roles only, meaningless outside the tenant.
- Vendor lock-in; per-seat pricing at scale.

**Relation to Verana.** Complementary, and say so on stage: keep Entra/Okta for internal governance, plug the organization into the trust layer for everything that crosses its boundary. Bridge: register the org's DID as a VPR Corporation, bind Entra-managed agents to it via operator credentials.

---

## 2. Agent directories

**Examples.** A2A Agent Cards, the MCP Registry, AGNTCY Agent Directory (Cisco-initiated; IPFS DHT + OCI + Sigstore, OASF schema), NANDA Index / AgentFacts (MIT), Agent Name Service (ANS) IETF draft.

**What it is.** Discovery layers: machine-readable descriptors of what an agent is called, where it lives, what it can do, and which keys it uses, published in registries or on domains so other agents can find and call it.

**Pros.**
- Solve a real, unsolved problem (discovery) and are transport-native: A2A and MCP tooling reads them directly.
- Lightweight to publish and consume; low barrier to entry.
- Some (AGNTCY) add signing and provenance (Sigstore) and separate capability from permission conditions (OASF).
- Open source, community-driven, moving fast.

**Cons.**
- Self-declared: the descriptor says what the publisher wants it to say. No third party vouches for any claim.
- No operator binding: nothing links the agent to a legal entity that answers for it.
- Capability claims are unverified; no accreditation or authorization semantics.
- Trust root is usually web PKI or the registry host: observer properties vary by host and are not designed for privacy.
- Ranking/discovery is popularity- or listing-based, gameable like SEO.

**Relation to Verana.** Complementary lower layer: a directory tells you an agent EXISTS and how to reach it; Verana tells you whether to TRUST it. Bridge: Trust Graph results can be exposed alongside directory entries; agent cards can carry the DID that Verana trust resolution starts from.

---

## 3. Bot attestation

**Examples.** Cloudflare Web Bot Auth (IETF HTTP Message Signatures track), adopted into payment-network agent authentication by Visa, Mastercard and American Express (October 2025); CDN "verified bot" directories.

**What it is.** Cryptographic request signing that lets an origin (or CDN/WAF in front of it) distinguish a known, registered bot or agent from an anonymous scraper: the agent signs HTTP requests, and the receiving edge checks the signature against a directory of registered agents.

**Pros.**
- Deployed at internet scale already (Cloudflare edge), pragmatic, and solves an acute problem for site owners drowning in AI crawlers.
- On a standards track (IETF), with real payment-industry uptake.
- Cheap for agent operators to adopt; no wallet or credential infrastructure required.

**Cons.**
- Binary trust: "this is a known bot from directory X". No identity of the operator as a legal entity, no scoping of what it may do, no accreditation.
- The directory operator is a central chokepoint AND observer: it decides who counts as legitimate and sees verification traffic.
- Governance is the directory owner's commercial policy, not a community's published rules.
- Nothing for the reverse direction: the agent cannot verify the service.

**Relation to Verana.** Attestation of transport-level authenticity, not trust. Compatible: a request could be Web-Bot-Auth-signed AND carry a DID whose Verifiable Trust resolution provides operator + accreditation. Position as "necessary traffic hygiene, not an identity layer".

---

## 4. On-chain agent registries

**Examples.** ERC-8004 "Trustless Agents" (proposed August 2025, Ethereum mainnet deployment January 29, 2026; Identity Registry as ERC-721, plus Reputation and Validation registries; rollouts on Base and other L2s in progress).

**What it is.** Agent identity as an on-chain asset: an agent registers an NFT-based identity once per chain, counterparties leave publicly readable feedback (reputation) and independent attestations of performance (validation), and higher-level systems consume these registries.

**Pros.**
- Genuinely decentralized: no tenant, no directory owner, no observer in the verification path. The only other "Yes" in the deck's no-observer column, and credit it on stage.
- Portable, censorship-resistant identity; open permissionless innovation; composable with on-chain payments (x402 and friends).
- Real momentum in the crypto-agent economy; reference implementations live.

**Cons.**
- Pseudonymous by design: no binding to a legal entity, so no accountability when an agent misbehaves beyond burning its reputation.
- Reputation is not accreditation: scores measure past feedback (gameable, sybil-prone, bootstrapping problem), not authorization by a governing body.
- No governance semantics: nothing expresses "who may issue what" or sector rules.
- Ecosystem skews to crypto-native use; enterprises and regulators are structurally uncomfortable with pseudonymous accountability.
- Everything is public forever: reputational data on-chain has its own privacy problems.

**Relation to Verana.** The philosophical cousin on decentralization with the opposite trust model: reputation vs accountable authorization. Not a bridge priority; useful contrast slide-side ("decentralized, but accountability replaced by reputation").

---

## 5. Payment agent programs

**Examples.** Visa Trusted Agent Protocol (TAP, launched October 2025 with Cloudflare: signed agent identity + intent tokens checked against a Visa-operated directory), Google Agent Payments Protocol (AP2, extension of A2A, with verifiable-credential "mandates" carrying user authorization), Mastercard agentic tokens, plus commerce protocols (ACP, UCP) around them.

**What it is.** The payment networks' answer to "is this a real agent acting for a real customer?": agents register with the scheme, sign their shopping/payment intents, and merchants verify against the scheme's directory before honoring agent-initiated transactions.

**Pros.**
- Massive distribution: the schemes can push this to every merchant they already reach.
- AP2's mandates use W3C Verifiable Credentials: strong validation of the VC-based approach, with real user-authorization semantics (what did the human actually approve?).
- Solves a concrete liability problem (chargebacks, fraud) with clear economic incentives.

**Cons.**
- Sectoral silo: commerce only. The trust established is meaningless outside the payment flow.
- Per-scheme central directories: registration with, and observation by, each network; the deck's "N sectors × M platforms" pattern in its purest form.
- Operator binding is "registered with the network", under the scheme's private rules, not publicly verifiable governance.
- Multiple competing protocols (TAP vs AP2 vs ACP) already fragment the silo internally.

**Relation to Verana.** The strongest proof that sector players will build sectoral trust registries if no common layer exists. Bridge: a payments ecosystem on Verana could anchor the same mandates/schemas publicly; AP2's VC mandates could be issued/verified under ecosystem permissions.

---

## 6. Trust registry networks

**Examples.** Ayra Association (registry-of-registries network from the ToIP/GAN lineage; Trust Registry Query Protocol, TRQP, for cross-ecosystem authorization checks; Credential Engine joined June 2026), DeDi / dedi.global (LFDT Labs + Networks for Humanity + Dhiway: signed JSON registry files on the publisher's domain, "DNS for Trust").

**What it is.** The closest cousins: infrastructure for publishing and querying WHO is recognized to do WHAT in an ecosystem: authoritative lists of issuers, members, licenses, revocations, plus query protocols to check recognition across ecosystems.

**Pros.**
- Right conceptual frame: ecosystems, authorization, recognized issuers, cross-domain recognition.
- Ayra/TRQP carries governance credibility from the ToIP body of work; a real network of registries is forming.
- DeDi is radically simple to adopt (signed files on your own domain), free, and web-native.
- Both are open and non-commercial in spirit: allies, not adversaries.

**Cons.**
- Query-time lookups: verification typically asks a registry endpoint, which can observe who asks about whom (weaker privacy than local resolution over replicated state).
- DeDi has no authorization semantics at all: it proves what a domain PUBLISHES, not who is ENTITLED to publish it; trust root is web PKI.
- Registry entries are about issuers/organizations, not about agents on transports: no Proof-of-Trust at connection time, no agent story out of the box.
- No discovery/ranking layer, no economic layer to sustain registry operation.

**Relation to Verana.** Most complementary of all rows. Bridges: Verana can answer TRQP queries (x401 proposal), export ecosystems as DeDi files, and accept such lists as evidence. On stage: "closest cousins, and we build bridges, not walls."

---

## 7. Verana · Verifiable Trust (honest self-assessment)

**What it is.** Open, decentralized trust infrastructure: trust ecosystems publish machine-readable governance (credential schemas, roles, issue/verify permissions) on a public Verifiable Public Registry; services and agents present DIDs + verifiable credentials binding them to accountable legal entities; peers run Proof-of-Trust client-side before data flows; the Trust Graph makes trust discoverable (API/MCP). Apache 2.0, live on testnet.

**Pros (the four columns).**
- Who it is: DID on any transport (HTTPS, MCP, A2A, DIDComm).
- Who operates it: credential chain to a legal entity: accountability, not reputation.
- What it may do: ecosystem accreditations under public, auditable permission trees.
- No central observer: trust resolution is a local computation over public replicated state + peer-presented credentials; no call home, no beacon.
- One layer for every actor type (wallet, service, IoT, org, agent) and every sector: differences live in models (schemas, roles, governance), not in parallel infrastructures.
- Conformance-testable normative spec (ODC-Tester collaboration with Trialog).

**Cons (be honest, especially in this room).**
- Early: testnet, not mainnet; adoption is the whole game and network effects are unproven.
- Spec still evolving (v4 in delivery); rich delegation/mandate semantics (PoA-style) deliberately deferred until after v4, though they are only a credential schema away.
- A public permissioned registry invites the "why a ledger?" objection: the answer (shared state without an operator-observer) must be made every time.
- Ecosystem governance is powerful but demands work from adopters: someone must write the schemas and rules.
- Small team and foundation vs hyperscaler distribution.

---

## Adjacent: architecture papers and frameworks (not in the table: proposals, not deployments)

- **Spherity "Beyond Zero Trust: M-Trust" (Carsten Stöcker, 2026-09-16).** 8-layer architecture for cross-domain agent authorization; independently derives the Verifiable Trust requirements (verifiable authority chains, verifier sovereignty, no universal broker) and calls for trust registries, technical profiles and conformance tests. Strongest third-party validation to date; its PoA attribute set (purpose, limits, time window, geography, delegation depth, termination) is the checklist for Verana's post-v4 delegation schema.
- **CSA Agentic Trust Framework (massivescale-ai, v0.9.1 public review April 2026).** Zero-Trust governance spec for autonomous agents; enterprise-compliance flavored; watch for v1.0.
- **GSMA agentic AI security work (M-Trust drafts, MWC 2026 track).** Telco framing of the same convergence; drafts not yet public in detail.

**The convergence point (use it as the closing argument):** every serious effort, enterprise, on-chain, payments, registries, papers, converges on the same requirements: strong agent identity, accountable operators, scoped authorization, verifiable evidence, decisions at the verifier. They differ in scope and observer properties. Verana's claim is not that the others are wrong: it is that these requirements deserve one open, privacy-preserving layer instead of a silo per vendor and sector.

---

*Sources: vendor GA announcements and docs (Okta, Microsoft, AWS), EIP-8004 and deployment trackers, Google Cloud AP2 announcement, Visa TAP / Cloudflare press (Oct 2025), IETF drafts (Web Bot Auth, ANS v2), Ayra Association resources, LFDT DeDi repos, Spherity research index, arXiv 2508.03095 (agent registry survey). Compiled 2026-09-17 for the Eclipse Models for Privacy webinar.*
