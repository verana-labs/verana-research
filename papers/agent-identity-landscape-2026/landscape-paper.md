# The Agent Identity Landscape, September 2026

*A comparative analysis of trust approaches for autonomous actors*

**Fabrice Rochette** · The Verana Foundation
**Ariel Gentile** · 2060 OÜ

*September 2026 · License: CC BY 4.0*

*Companion paper to the talk "[Why AI Agents Must Have Their Own Identity?](https://github.com/verana-labs/verana-research/blob/main/webinars/2026-09-17-eclipse-models-for-privacy/verana-verifiable-trust-eclipse-webinar-v4.html)", Eclipse Models for Privacy Interest Group webinar, September 17, 2026.*

---

## Abstract

AI agents increasingly initiate connections, invoke tools, and exchange personal data across organizational boundaries with no human in the loop, yet no widely deployed mechanism lets a counterparty verify who an agent is, which legal entity operates it, and what it is authorized to do. During 2025 and 2026 a rich landscape of partial answers has emerged: enterprise identity platforms extended to agents, agent directories, bot attestation schemes, on-chain agent registries, payment-network agent programs, and trust registry networks. This paper surveys these six families of approaches and evaluates each against four criteria derived from first principles: verifiable identifier, accountable operator, verifiable authorization, and absence of a central observer. We find that every approach solves a genuine slice of the problem while none satisfies all four criteria, and that the most common architectural choice, a central directory or tenant, structurally reintroduces the privacy threats that the LINDDUN framework classifies as linking, detecting, and data disclosure. We argue that agent identity is not a special case: services, organizations, IoT devices, and personal user agents require the same verifiable statements, and sector-specific registry schemes differ in their governance models rather than in their infrastructure needs. We conclude by describing Verifiable Trust, an open, decentralized trust layer in which sovereign ecosystems accredit participants, proof is attached publicly to decentralized identifiers, verification is a mutual, client-side computation, and public proof becomes searchable, and we assess it honestly against the same four criteria, including its current limitations.

## 1. Introduction

The inflection to agentic software is no longer prospective. Autonomous agents built on generative AI already act on behalf of people and organizations: they initiate connections, call tools over protocols such as the Model Context Protocol (MCP) and Agent2Agent (A2A), transact, and carry delegated authority into services their principals never see. Every such interaction requires an answer, at machine speed, to a question the current internet cannot answer: *who is this, and should data flow?*

Transport security does not answer it. A TLS certificate binds a key to a domain name; it proves neither the legal entity behind an endpoint nor what that entity is authorized to do. Platform accounts do not answer it either: an agent is not its user, and a tenant-scoped identity is meaningless outside the tenant.

We take as a starting point that an agent's identity must make three statements verifiable by any counterparty, before any data flows:

1. **Who it is.** An identifier the agent itself controls, resolvable and verifiable by anyone, on any transport.
2. **Who operates it.** A verifiable binding to the legal entity that runs the agent and answers for it.
3. **What it may do.** Verifiable authorizations, granted by communities competent to grant them.

To these we add a fourth requirement, drawn from privacy engineering: the verification itself must not create a new observer. If every trust check routes through a central platform, that platform accumulates the relationship graph of the entire ecosystem. In the terminology of the LINDDUN privacy threat modeling framework [12], such a design builds in *linking* (the broker correlates who connects to whom), *detecting* (the fact of a connection is itself sensitive), and *data disclosure* (relationship metadata concentrates at one point of failure). A trust layer that fails its own privacy threat model is not a solution; it is the surveillance problem relocated one layer up.

**Contributions.** This paper (i) proposes a compact evaluation framework for agent identity approaches; (ii) surveys six families of deployed systems as of September 2026 and evaluates them against the framework; (iii) reviews adjacent architecture proposals and documents a striking convergence of requirements across independent efforts; (iv) argues that agent identity, service identity, organizational identity, and IoT identity are the same problem, and that sector differences reduce to governance models; and (v) presents and honestly assesses Verifiable Trust, an open infrastructure designed to satisfy all four criteria at once.

**Scope and stance.** All six families surveyed here are serious, recent work solving real problems; several are complementary to one another and to the approach we present. The purpose of the comparison is not ranking for its own sake but locating the gap that remains when all of them are deployed together.

## 2. Evaluation Framework

Each approach is evaluated on four questions.

**C1 · Who it is.** Does the approach give the agent an identifier it controls, verifiable by any party, portable across transports and organizational boundaries?

**C2 · Who operates it.** Does it bind the agent to an accountable legal entity, in a way a stranger can verify without a business relationship with the platform that made the binding?

**C3 · What it may do.** Does it express authorizations with governance semantics: who granted the right, under which published rules, revocable and auditable?

**C4 · No central observer.** Can a counterparty verify C1 through C3 without a third party learning that the verification happened? This criterion operationalizes the LINDDUN threats of linking and detecting for trust infrastructure itself. It implies, in practice, that verification must be computable locally from public state and peer-presented evidence, and that verification must be possible *mutually*: both peers verify each other before connecting.

## 3. The Landscape

### 3.1 Enterprise agent IAM

**Representatives.** Microsoft Entra Agent ID (generally available with Agent 365, spring 2026); Okta for AI Agents (GA April 2026, with Amazon Bedrock AgentCore integration); AWS AgentCore Identity; the Cross App Access (XAA) semantics added to the MCP specification (November 2025) [1] [2].

**What it is.** The enterprise identity and access management stack extended to non-human identities: each agent receives a directory identity in the organization's tenant, with lifecycle management, conditional access, least-privilege policies, and anomaly detection.

**Strengths.** Mature and operational; genuine lifecycle governance; deep integration with the policy engines enterprises already run. For the intra-organizational question, which of *our* agents may touch which of *our* systems, this is the right tool.

**Limitations.** Identity and trust stop at the tenant boundary. Cross-organization trust is bilateral administrator configuration inside a vendor's hub; an outside counterparty can verify nothing independently. The platform observes all authentication traffic (fails C4). There is no binding to a legal entity that a stranger can check (C2 partial at best), and internal roles carry no meaning outside the tenant (C3 fails externally).

### 3.2 Agent directories

**Representatives.** A2A Agent Cards; the MCP Registry; the AGNTCY Agent Directory (IPFS DHT, OCI, Sigstore, with the OASF schema separating capability from usage conditions); the NANDA Index / AgentFacts (MIT); the Agent Name Service (ANS) IETF draft [3] [4].

**What it is.** Discovery layers: machine-readable descriptors of what an agent is called, where it is reachable, what it claims to be able to do, and which keys it uses.

**Strengths.** They address discovery, a real and otherwise unsolved problem, and are transport-native: A2A and MCP tooling consumes them directly. Some add signing and provenance. Barriers to publication are low, which fits an ecosystem that is growing fast.

**Limitations.** Descriptors are self-declared; no third party vouches for any claim. There is no operator binding (C2 fails) and no authorization semantics (C3 fails): capability claims are assertions, not accreditations. Trust roots are typically web PKI or the registry host, and observer properties vary by host (C4 undetermined). A directory tells you an agent *exists*; it cannot tell you whether to *trust* it.

### 3.3 Bot attestation

**Representatives.** Cloudflare Web Bot Auth (HTTP Message Signatures, IETF track), adopted into payment-network agent authentication by Visa, Mastercard, and American Express in October 2025 [5].

**What it is.** Cryptographic request signing that lets an origin, or the CDN in front of it, distinguish a registered agent from an anonymous scraper, by checking request signatures against a directory of known agents.

**Strengths.** Deployed at internet scale; pragmatic; standards-track; solves an acute operational problem for site owners, and cheaply for agent operators.

**Limitations.** Trust is binary ("a known bot from directory X"): no legal-entity identity (C2 fails), no scoped authorization (C3 fails). The directory operator is both chokepoint and observer (C4 fails), and its admission policy is commercial rather than published governance. Verification is one-directional: the agent cannot verify the service.

### 3.4 On-chain agent registries

**Representatives.** ERC-8004 "Trustless Agents" (proposed August 2025; Ethereum mainnet deployment January 2026; Identity Registry as ERC-721 plus Reputation and Validation registries) [6].

**What it is.** Agent identity as an on-chain asset: portable, censorship-resistant registrations, with publicly readable feedback (reputation) and third-party attestations (validation) consumable by higher-level systems.

**Strengths.** Genuinely decentralized: no tenant, no directory owner, no observer in the verification path. This family is the only one besides the approach of Section 6 that satisfies C4. Composable with on-chain payment rails; reference implementations are live.

**Limitations.** Identities are pseudonymous by design: there is no binding to an accountable legal entity (C2 fails), so accountability reduces to reputation at stake. Reputation is not accreditation (C3 fails): scores aggregate past feedback, which is sybil-prone and gameable, and encode no governance ("who may issue what" is inexpressible). Public-forever reputational data raises its own privacy questions.

### 3.5 Payment agent programs

**Representatives.** Visa Trusted Agent Protocol (TAP, October 2025, with Cloudflare); Google's Agent Payments Protocol (AP2), an A2A extension whose "mandates" carry user authorization as W3C Verifiable Credentials; Mastercard agentic tokens; the surrounding commerce protocols (ACP, UCP) [7] [8].

**What it is.** The payment networks' answer to "is this a real agent acting for a real customer?": agents register with a scheme, sign their intents, and merchants verify against the scheme's directory before honoring agent-initiated transactions.

**Strengths.** Distribution through networks that already reach every merchant; concrete liability incentives; and, in AP2's case, strong validation of the verifiable-credential approach, with real user-authorization semantics.

**Limitations.** A sectoral silo: trust established for commerce is meaningless outside the payment flow (C3 scoped to one domain). Identity is per-scheme (C1 partial) and operator binding means "registered with the network" under private rules (C2 partial). Each scheme runs a central directory that registers and observes participants (C4 fails). The silo is already fragmenting internally across competing protocols.

### 3.6 Trust registry networks

**Representatives.** The Ayra Association network (registry-of-registries from the Trust over IP lineage, with the Trust Registry Query Protocol, TRQP, for cross-ecosystem authorization checks); DeDi / dedi.global (signed JSON registry files served from the publisher's own domain) [9] [10].

**What it is.** Infrastructure for publishing and querying who is recognized to do what within an ecosystem: authoritative lists of issuers, members, licences, and revocations, plus protocols to check recognition across ecosystems.

**Strengths.** The right conceptual frame: ecosystems, authorization, recognized issuers, cross-domain recognition. Ayra carries governance credibility and a forming network of registries; DeDi is radically simple to adopt and web-native. These are the closest relatives of the approach in Section 6, and largely complementary to it.

**Limitations.** Verification is typically a query-time lookup against a registry endpoint, which can observe who asks about whom (C4 weakened relative to local resolution over replicated state). DeDi proves what a domain *publishes*, not who is *entitled* to publish it, and carries no authorization semantics (C3 fails for DeDi). Registry entries concern issuers and organizations rather than agents on transports: there is no proof exchanged at connection time and no agent story out of the box (C1 not addressed). Neither family includes a discovery or ranking layer.

## 4. Comparative Summary

| Approach | C1 · Who it is | C2 · Who operates it | C3 · What it may do | C4 · No central observer |
|---|---|---|---|---|
| Enterprise agent IAM | Tenant-scoped ID | The tenant itself | Internal roles only | No: hub observes all |
| Agent directories | Keys and names | Self-declared | Capability claims, unverified | Varies by host |
| Bot attestation | Signed requests | Directory vouches | Binary: known bot | No: central directory |
| On-chain agent registries | Portable token ID | Pseudonymous | Reputation scores | Yes |
| Payment agent programs | Per-scheme ID | Registered with the network | Commerce only | No: scheme directory |
| Trust registry networks | Lists about issuers | Registry entries | Authorization lookups | Query-time lookup |

Each family covers a genuine slice: tenant governance, discovery, bot attestation, decentralized reputation, payment liability, or authoritative lists. None binds an agent to an accountable operator, with verifiable authorizations, across domains, without an observer. That full combination is the gap.

## 5. Adjacent Architecture Proposals and the Convergence Finding

Beyond deployed systems, 2026 has produced architecture work that is best read as requirements analysis. Spherity's "Beyond Zero Trust: M-Trust" (September 2026) argues that single-enterprise Zero Trust cannot authorize agents across companies and jurisdictions, and derives an architecture of verifiable authority chains from authoritative source through legal person, authorized representative, agent, and task mandate to a verifier-side decision and a signed receipt, with explicit "verifier sovereignty" (no external party decides access for the relying domain) and no universal hierarchy [11]. The Cloud Security Alliance's Agentic Trust Framework and the GSMA's agentic-AI security work frame comparable requirements for enterprise compliance and telecommunications respectively.

The notable fact is convergence. Independent efforts from enterprise identity, blockchain, payments, registry networks, and standards bodies arrive at the same requirement set: strong agent identity, accountable operators, task-scoped and verifiable authorization, decisions made at the verifier, evidence that outlives the interaction. They differ in scope and, critically, in observer properties. The requirements are no longer controversial; what is missing is one open, privacy-preserving layer that satisfies them together, and the conformance profiles and test suites to hold implementations to it.

## 6. One Layer: Verifiable Trust

### 6.1 The same problem, again

Before presenting the layer, one observation dissolves most of the landscape's fragmentation. The three statements of Section 1 are not specific to AI agents. An online service must prove its identifier, its legal operator, and its sector authorizations. An IoT device must prove its identifier, its manufacturer, and its conformity attestations. An organization must prove its registration and memberships; a personal user agent proves its holder's credentials. Meanwhile each sector stands up its own scheme, payment networks run agent directories, education runs credential registries, health runs provider directories, public administrations run trusted lists, and each re-solves identifier, operator, and authorization for one vertical. What actually differs between these cases is the *governance model*: which credentials exist, who may issue and verify them, under which rules. The infrastructure, registries, resolution, proof exchange, and search, is common. Building it once, and letting ecosystems differ where they actually differ, is the design thesis of Verifiable Trust.

### 6.2 The concept

Verifiable Trust [13] is an open, decentralized trust infrastructure whose mechanics unfold as a causal chain:

1. **Ecosystems define trust in their domain.** A trust ecosystem is a community, a sector body, a government program, a company network, that publishes machine-readable governance: an Ecosystem Governance Framework anchored to the ecosystem's DID, credential schemas (the data model each credential must satisfy), and a participant tree recording who is accredited to issue and to verify each schema, with delegation and revocation in public.
2. **Anyone can create or join an ecosystem.** Creation is permissionless; participation is a choice. Sector rules stay sector-owned on shared rails.
3. **Participants join to be accredited, or to hold credentials.** A single identity can be an accredited issuer of one schema in one ecosystem, an accredited verifier of another schema in another, and a holder of credentials from a third.
4. **Proof is attached publicly to the identifier.** Credentials and accreditations are linked to the DID itself, as verifiable presentations in or linked from the DID document. Resolving the identifier *is* seeing the proof: no account, no API gatekeeper, the same attachment serving MCP, A2A, DIDComm, and plain HTTPS.
5. **Peers verify each other before connecting.** Proof-of-Trust is mutual: each peer resolves the other's DID and presentations, verifies signatures and schemas locally, and checks the other's issuers and verifiers against the ecosystem's public, replicated registry state. The connection proceeds only if the applicable governance rules pass on both sides; private credentials, if any, are exchanged only afterward, over the established channel. Every input is public or presented by the peers themselves; no issuer is called, no status beacon fired, no third party learns the check happened.
6. **Public proof is searchable proof.** Because attachment is public, the network is indexable: one queryable graph of identifiers, accreditations, and ecosystems, in which services and agents are found by the credentials they hold and by who accredited them, ranked by verifiable trust signals rather than by advertising or search-engine optimization.

Against the framework: C1 is a DID on any transport; C2 a credential chain to a legal entity, accountability rather than reputation; C3 ecosystem accreditations under public, auditable participant trees; C4 mutual, client-side resolution over public state.

### 6.3 Honest assessment

A comparison is credible only if the proposing side is examined by the same criteria, so we state where Verifiable Trust stands today. The network runs on a public testnet, with mainnet ahead; like any trust infrastructure, its value compounds with adoption, and the wallet integrations, reference ecosystems and use cases now running are the leading edge of that curve. The specifications are converging on their next major version; richer delegation and mandate semantics of the kind M-Trust describes (purpose, value limits, time windows, delegation depth, termination) are intentionally sequenced after it, and on this architecture they amount to an additional credential schema rather than a protocol change. A public ledger-based registry raises a fair and recurring question, "why a ledger?", to which the answer is precise: shared, replicated public state is what removes the operator-observer, and we know of no lighter construction that preserves criterion C4 at internet scale. Ecosystem governance asks real work of adopters, schemas and rules must be written: that is the cost of sector sovereignty, and reference ecosystems and tooling exist to reduce it. Finally, the infrastructure is stewarded by a non-profit foundation rather than a platform vendor: a deliberate design choice for neutral infrastructure, with the trade-offs in reach that this implies. These are the costs of satisfying the four criteria as we currently understand them; we state them so that the comparison of Section 4 can be audited rather than believed.

## 7. Conclusion

The agent identity landscape of 2026 is rich, serious, and partial. Enterprise IAM governs the inside of organizations; directories make agents findable; attestation separates known bots from scrapers; on-chain registries prove that decentralized agent identity is practicable; payment programs demonstrate distribution and validate verifiable credentials; registry networks carry the right governance concepts. None of them, alone or in combination, binds an agent to an accountable operator with verifiable, governed authorizations, across domains, without creating a new observer, and the architecture literature now converges on precisely that requirement set. We have argued that the requirement set is not agent-specific but universal across services, organizations, devices, and people's agents, that sector differences are governance models rather than infrastructures, and that one open, privacy-preserving layer, of which Verifiable Trust is a running, testable implementation, can carry them all. The near-term work is community-shaped: privacy threat analysis of the specifications with the LINDDUN framework, alignment of credential schemas and ecosystem roles with the W3C Data Protection Vocabulary [14], and independent conformance testing of implementations, of the kind pursued with Trialog's ontology-driven constraint tester in the Eclipse ecosystem. The specifications, code, and network are open; scrutiny is invited.

## References

[1] Okta, "Okta for AI Agents" and press materials on agent identity security, 2026. https://www.okta.com/products/govern-ai-agent-identity/

[2] Microsoft, "Microsoft Entra Agent ID" documentation, and "Announcing Microsoft Entra Agent ID," Microsoft Entra blog. https://learn.microsoft.com/en-us/entra/agent-id/ · https://techcommunity.microsoft.com/blog/microsoft-entra-blog/announcing-microsoft-entra-agent-id-secure-and-manage-your-ai-agents/3827392

[3] AGNTCY, "Identity: onboard, create and verify identities for agents, MCP servers and multi-agent systems." https://github.com/agntcy/identity

[4] R. Narajala, C. Courtney, "Agent Name Service v2 (ANS): A Domain-Anchored Trust Layer for Autonomous AI Agent Identity," IETF Internet-Draft. https://datatracker.ietf.org/doc/html/draft-narajala-courtney-ansv2

[5] Cloudflare, "Securing agentic commerce: helping AI agents transact with Visa and Mastercard," Cloudflare blog, and press release, October 14, 2025. https://blog.cloudflare.com/secure-agentic-commerce/ · https://www.cloudflare.net/news/news-details/2025/Cloudflare-Collaborates-with-Leading-Payments-Companies-to-Secure-and-Enable-Agentic-Commerce/default.aspx

[6] Ethereum Improvement Proposals, "ERC-8004: Trustless Agents." https://eips.ethereum.org/EIPS/eip-8004

[7] Google Cloud, "Announcing Agent Payments Protocol (AP2)," 2025. https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol

[8] Visa, "Visa Introduces Trusted Agent Protocol: An Ecosystem-Led Framework for AI Commerce," press release, October 14, 2025. https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html

[9] Ayra Association, trust registry resources and whitepapers. https://github.com/ayraforum/ayra-trust-registry-resources · https://ayra.forum/whitepapers/

[10] LF Decentralized Trust Labs, "Decentralized Directory Protocol (DeDi)." https://dedi.global

[11] C. Stöcker, "Beyond Single-Enterprise ZTA: Multi-Trust Architectures for Authorised Agentic Actors," Spherity Research, September 16, 2026. https://spherity.github.io/spherity-research/beyond-zero-trust-m-trust-authorised-agentic-actors.html

[12] K. Wuyts, W. Joosen et al., "LINDDUN privacy threat modeling framework," KU Leuven DistriNet. https://linddun.org · referenced in ISO/IEC TS 27564:2025.

[13] Verana Labs, "Verifiable Trust Specification" and "Verifiable Public Registry Specification." https://verana-labs.github.io/verifiable-trust-spec/ · https://verana-labs.github.io/verifiable-trust-vpr-spec/

[14] H. J. Pandit et al., "Data Privacy Vocabulary (DPV)," W3C Data Privacy Vocabularies and Controls Community Group. https://w3id.org/dpv

[15] "Evolution of AI Agent Registry Solutions: Centralized, Enterprise, and Decentralized Approaches," arXiv:2508.03095, 2025. https://arxiv.org/abs/2508.03095

---

*© 2026 The Verana Foundation. Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0). Comments and corrections: https://github.com/verana-labs/verana-research.*
