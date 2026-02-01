# 🎬 IBM TrustBuild — 2-Minute Demo Script

> **Video Title:** IBM TrustBuild: From Idea to Compliant Deployment in 60 Seconds
> **Total Duration:** 120 seconds (2:00)
> **Format:** Screen recording with voiceover (split-screen optional)

---

## [0:00 – 0:15] The Hook

**Visual:**
- Quick montage: complex cloud architecture diagram → "Deployment Denied" red stamp → developer looking frustrated at blank screen → compliance checklist with red X marks

**Audio:**
> "In the enterprise, the fastest way to kill a great idea is a slow compliance review. Developers want speed. The business needs safety. What if you could have both?"

---

## [0:15 – 0:35] The Reveal

**Visual:**
- Open the **IBM TrustBuild dashboard** (full screen)
- Show the clean prompt input area
- IBM TrustBuild branding and header visible
- Point out the "watsonx.ai + Granite 3.0" badge in the top bar

**Audio:**
> "Introducing IBM TrustBuild. We've used watsonx.ai and Langflow to create an AI-powered architect that doesn't just write code — it enforces governance at the source. Let's see it in action."

---

## [0:35 – 1:00] Step 1 & 2: Architecting

**Visual:**
- Click the example prompt chip: *"Build a customer portal that uses AI to analyze sensitive health data"*
- The prompt fills the text area
- Click **🚀 Run TrustBuild**
- Watch Stage 1 (Intent Extraction) light up with the blue "running" animation
  - Expand it to show: **Sensitivity: PHI** detected, **Frameworks: HIPAA, IBM_BASELINE**
- Stage 2 (Architecture Mapping) activates next
  - Expand to show the IBM Cloud services grid: **Code Engine, Cloudant (dedicated), watsonx.ai, VPC**

**Audio:**
> "Watch as our Architect Agent analyzes the prompt. Using IBM Granite 3.0, it immediately identifies this as a PHI workload — Protected Health Information. It maps out a secure stack on IBM Cloud: serverless compute, a dedicated Cloudant database, and watsonx.ai for the AI layer. But because we mentioned 'sensitive health data,' the system knows this isn't a standard build."

---

## [1:00 – 1:30] Step 3: The Guardrail in Action ⚡

**Visual:**
- Stage 3 (Governance Guardrail) activates with the pulsing blue ring
- The status changes — pause here for impact
- The **Governance Panel** section appears below the pipeline
- Show the **compliance score bar** animating to **95%**
- Show the violation card:
  - 🔴 **[POL-HIPAA-001] Database VPC Isolation Required** — CRITICAL
  - Description: "PHI data stores must be isolated within a VPC..."
  - 🟢 **Auto-Correction:** "Enabled VPC isolation and configured private endpoints..."
- The stage badge reads: **↻ AUTO-CORRECTED** in yellow

**Audio:**
> "This is the Governance Guardrail — our innovation layer. Before generating a single line of code, our Auditor Agent catches a critical compliance risk. The proposed Cloudant database wasn't VPC-isolated — a HIPAA violation. Instead of stopping and failing, TrustBuild automatically refactors the architecture. We've turned the 'No' from the compliance team into an 'Auto-Correct' from the AI."

---

## [1:30 – 1:50] Step 4: Deployment Ready

**Visual:**
- Stage 4 (Secure Code Synthesis) completes with a green checkmark
- The **Deployment Kit** section appears with the green border
- Show the summary bar: **✓ Completed | 2.4s | ↻ Auto-Corrected | 5 files**
- Click open each file card to reveal:
  - 📦 **Dockerfile** — security-hardened with non-root user, TLS enforcement
  - 🏗️ **main.tf** — Terraform with VPC, Cloudant (dedicated), Key Protect
  - 🐍 **main.py** — FastAPI with IBM Cloudant + watsonx SDKs pre-configured
  - 📝 **requirements.txt** — IBM Cloud SDKs included
  - 📄 **README.md** — project docs with architecture table
- Scroll down to show the **IBM Cloud CLI Commands** block

**Audio:**
> "Finally, Granite-20b-code generates the full deployment kit. A security-hardened Dockerfile, Terraform infrastructure-as-code, and a FastAPI application with all IBM SDKs pre-configured. Five files, ready to deploy. What used to take a team a weekend now takes sixty seconds."

---

## [1:50 – 2:00] The Closer

**Visual:**
- Full-screen IBM TrustBuild logo/branding
- Text overlay: *"Faster. Safer. Built on watsonx."*
- IBM Dev Day: AI Demystified branding

**Audio:**
> "IBM TrustBuild: Bridging the gap from idea to deployment with the power of trusted AI. Innovation and compliance, in the same workflow. Let's build the future with confidence."

---

## 💡 Recording Pro-Tips

1. **The "Money Shot":** Make sure the Governance Guardrail section is clearly visible when the violation is detected and auto-corrected. This is your differentiation moment — linger on it.

2. **Show the Langflow Export:** If you have time, open `langflow/trustbuild_pipeline.json` in Langflow and show the visual node graph. IBM judges love seeing the orchestration layer.

3. **Audio Quality:** Use a decent mic. Clear audio scores higher than fancy editing.

4. **The IBM Factor:** Keep the IBM Cloud dashboard or watsonx branding visible in the background. It proves feasibility and ecosystem alignment.

5. **Pacing:** The 1:00–1:30 section (Guardrail) is your strongest differentiator. Slow down here. Let the judge see the violation, the auto-correction, and the green badge clearly.

6. **Backup Plan:** If recording on a slow connection, run the pipeline once before recording to warm the cache, then re-run during the actual take.
