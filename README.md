<div align="center">

<img src="assets/profile-banner.svg" alt="Madhan Alagarsamy - Profile Banner" width="100%" />

<br/><br/>

[![Website](https://img.shields.io/badge/Website-netcorporation.site-0ea5e9?style=for-the-badge&logo=google-chrome&logoColor=white)](https://netcorporation.site)
[![GitHub](https://img.shields.io/badge/GitHub-madhanalagarsamy-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/madhanalagarsamy)
[![Security Audits](https://img.shields.io/badge/Security-Upstream%20Audits-8b5cf6?style=for-the-badge&logo=securityscorecard&logoColor=white)](#security-research--upstream-auditing)
[![Open Source](https://img.shields.io/badge/OSS-Core%20Contributor-10b981?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](#open-source-contributions)

<br/>

<p align="center">
  <b>Security Researcher</b> &bull; <b>Systems & AI Frameworks Engineer</b> &bull; <b>Founder of <a href="https://netcorporation.site">Net Corporation</a></b>
</p>

<p align="center">
  <sub>Specializing in upstream vulnerability discovery, defensive systems engineering, deep learning runtime optimizations, and air-gapped optical communication protocols.</sub>
</p>

---

[About Me](#about-me) &bull;
[Current Focus](#current-focus) &bull;
[Featured Projects](#featured-projects) &bull;
[Security Research](#security-research--upstream-auditing) &bull;
[Tech Stack](#tech-stack) &bull;
[GitHub Activity](#github-activity) &bull;
[Recent Work](#-recent-work) &bull;
[Connect](#connect-with-me)

---

</div>

## About Me

I am a Security Researcher, Systems & AI Engineer, and the Founder of **[Net Corporation](https://netcorporation.site)**. 

My work centers on identifying and mitigating critical software flaws in major open-source ecosystems, engineering high-assurance defensive software architectures, and optimizing deep learning frameworks. I direct Net Corporation's technology roadmap, secure code review desks, and project delivery pipelines.

Beyond applied security, I build resilient production systems—ranging from air-gapped screen-to-camera optical transfer channels using Luby Transform fountain codes to computer vision biometric verification and hardened web platforms.

---

## Current Focus

- 🛡️ **Vulnerability Research & Secure Code Review**: Auditing upstream machine learning and system libraries for arithmetic edge-case crashes, resource leaks, relative path traversals, and unverified CI/CD script executions.
- ⚡ **Deep Learning Framework Optimization**: Diagnosing runtime faults across distributed training (PyTorch DDP / Keras), quantization routines (GPTQ matrix division-by-zero resilience), and data loading pipelines.
- 📡 **Air-Gapped & Optical Data Transfer**: Advancing rateless Fountain Coding (Luby Transform) algorithms for high-throughput, screen-to-camera optical communication channels without network handshakes.
- 🔒 **Defensive Web Engineering**: Architecting hardened full-stack systems featuring multi-tier magic-byte file validation pipelines, atomic state-machine order workflows, and deterministic scheduling engines.

---

## Featured Projects

<table>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/madhanalagarsamy/decimal-optical-transfer">📡 Decimal Optical Transfer</a></h3>
      <p><b>Air-Gapped Screen-to-Camera Optical File Transmission</b></p>
      <p>Transmits up to <b>1 GB</b> of arbitrary files or text snippets between devices using purely a screen and a camera—zero Wi-Fi, zero Bluetooth, and zero pairing required.</p>
      <ul>
        <li><b>Fountain Coding (Luby Transform)</b>: Solves visual packet loss by streaming endless pseudorandom block combinations (XOR). Receiving any ~K &times; 1.15 frames fully rebuilds the payload.</li>
        <li><b>Duo-QR Mosaic & Real-Time Decoding</b>: 2x optical throughput optimization with CRC32 integrity verification and live browser stream reconstruction.</li>
      </ul>
      <p>
        <code>TypeScript</code> &bull; <code>Canvas API</code> &bull; <code>Fountain Codes</code> &bull; <code>Web Streams</code>
      </p>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/madhanalagarsamy/national-people-database-face-recognition-system">👁️ Biometric Face Recognition System</a></h3>
      <p><b>Biometric Citizen Record & Facial Verification Suite</b></p>
      <p>Comprehensive desktop biometric identity management application integrating real-time camera feeds, face detection bounding boxes, and dual-engine facial verification.</p>
      <ul>
        <li><b>Embedded Video Acquisition</b>: Real-time OpenCV video stream embedded directly in Tkinter UI with capture, preview, and confidence scoring.</li>
        <li><b>Transactional Database Engine</b>: Multi-criteria citizen search, profile registry, and structured SQLite3 data persistence.</li>
      </ul>
      <p>
        <code>Python</code> &bull; <code>OpenCV</code> &bull; <code>SQLite3</code> &bull; <code>Tkinter</code>
      </p>
    </td>
  </tr>
  <tr>
    <td colspan="2" valign="top">
      <h3><a href="https://github.com/madhanalagarsamy/creative-corner-ecommerce">🛍️ Creative Corner — Production E-Commerce Platform</a></h3>
      <p><b>Hardened Modular E-Commerce Backend & Scheduling Platform</b></p>
      <p>Production-grade e-commerce application engineered for bespoke handcrafted goods, custom artisan quotes, and deterministic fulfillment operations.</p>
      <ul>
        <li><b>4-Tier Magic Byte Validation</b>: Rigid customer file upload security verifying file signatures and MIME types against forged headers.</li>
        <li><b>Dynamic Lead Time & Quote Engine</b>: Multi-item preparation scheduling algorithm combined with atomic quote-to-order state machine transitions.</li>
      </ul>
      <p>
        <code>FastAPI</code> &bull; <code>SQLAlchemy 2.0</code> &bull; <code>Alembic</code> &bull; <code>Python 3.12+</code> &bull; <code>Jinja2</code>
      </p>
    </td>
  </tr>
</table>

---

## Security Research & Upstream Auditing

I actively audit and contribute patches to top-tier machine learning frameworks and distributed systems:

| Target & Ecosystem | Contribution / Security Audit | Impact & Link | Status |
| :--- | :--- | :--- | :---: |
| **PyTorch** (`pytorch/pytorch`) | **CI Security Review**: Unverified `curl \| sudo bash` pipe execution in `install_docs_reqs.sh` | Identified remote execution risk in docs build script &bull; [Issue #191843](https://github.com/pytorch/pytorch/issues/191843) | `Open` |
| **PyTorch** (`pytorch/pytorch`) | **Core Pooling Parameter Fix**: Fix `nn.LPPool1d` and `F.lp_pool1d` rejecting tuple/list `kernel_size` | Restored parameter compatibility with standard PyTorch pooling conventions &bull; [PR #191868](https://github.com/pytorch/pytorch/pull/191868) | `Open` |
| **PyTorch** (`pytorch/pytorch`) | **Profiler & ONNX Code Audits**: Syntax errors in profiler examples & ONNX non-tensor export | Fixed syntax and code execution examples &bull; [#190202](https://github.com/pytorch/pytorch/issues/190202), [#190203](https://github.com/pytorch/pytorch/issues/190203), [#190204](https://github.com/pytorch/pytorch/issues/190204), [#190199](https://github.com/pytorch/pytorch/issues/190199) | `Resolved` |
| **Keras** (`keras-team/keras`) | **Quantization Arithmetic Fix**: Division by zero in `gptq_quantize_matrix` | Fixed zero-denominator floating point arithmetic exception during matrix quantization &bull; [PR #23415](https://github.com/keras-team/keras/pull/23415) / [Issue #23413](https://github.com/keras-team/keras/issues/23413) | `Open` |
| **Keras** (`keras-team/keras`) | **Distributed Training Fix**: PyTorch DDP execution crashes, NCHW shape errors & sampler state | Resolved multi-GPU DDP training crashes and shape propagation &bull; [PR #23454](https://github.com/keras-team/keras/pull/23454) | `Open` |
| **Keras** (`keras-team/keras`) | **OpenVINO Backend Fix**: OpenVINO eigh Jacobi rotation convergence and test skip matching | Stabilized eigenvalue computation in OpenVINO backend &bull; [PR #23446](https://github.com/keras-team/keras/pull/23446) | `Merged` |
| **Keras** (`keras-team/keras`) | **Resource Leak Audit**: `CSVLogger` file descriptor leak on training failure/interrupt | Identified unclosed file handles on aborted execution &bull; [Issue #23354](https://github.com/keras-team/keras/issues/23354) | `Resolved` |
| **Keras** (`keras-team/keras`) | **Security & Path Traversal Review**: `ModelCheckpoint` relative traversal path validation | Evaluated arbitrary file write vectors in checkpoint paths &bull; [Issue #23312](https://github.com/keras-team/keras/issues/23312) | `Resolved` |
| **Keras** (`keras-team/keras`) | **Image Decompression Bomb Audit**: `load_img()` PIL `DecompressionBombError` handling | Audited denial-of-service vectors on maliciously oversized image uploads &bull; [Issue #23317](https://github.com/keras-team/keras/issues/23317) | `Open` |
| **Keras** (`keras-team/keras`) | **Execution Integrity**: Fail fast on invalid callbacks in `CallbackList` | Prevented silent training corruption and delayed `AttributeError` &bull; [PR #23368](https://github.com/keras-team/keras/pull/23368) / [Issue #23263](https://github.com/keras-team/keras/issues/23263) | `Merged` |
| **TensorFlow** (`tensorflow/tensorflow`) | **Keras Model Conversion**: Multi-decorator `tf.function` conversion fix | Resolved conversion failures when multiple decorators are present &bull; [PR #124545](https://github.com/tensorflow/tensorflow/pull/124545) | `Closed` |
| **TensorFlow** (`tensorflow/tensorflow`) | **Memory Safety**: Host memory (RSS) leak in `tf.data.Dataset.from_generator` | Documented host memory exhaustion during GPU pipeline iterations &bull; [Issue #123269](https://github.com/tensorflow/tensorflow/issues/123269) | `Resolved` |
| **BigBlueButton** (`bigbluebutton/bigbluebutton`) | **Concurrency Audit**: Race condition in `User.addStream()` duplicate stream IDs | Identified stream identifier collision under high-concurrency access &bull; [Issue #25544](https://github.com/bigbluebutton/bigbluebutton/issues/25544) | `Open` |
| **Future-AGI** (`future-agi/future-agi`) | **Security Disclosure & Reliability**: Private Vulnerability Reporting & OTLP Queue Bounding | Recommended GHSA adoption & bounded pending ingestion queue &bull; [Issue #2195](https://github.com/future-agi/future-agi/issues/2195) / [PR #2203](https://github.com/future-agi/future-agi/pull/2203) | `Open` |

---

## Tech Stack

<div align="center">

### Languages & Core
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=flat-square&logo=c%2B%2B&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-336791?style=flat-square&logo=sqlite&logoColor=white)

### AI, ML & Computer Vision
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=flat-square&logo=keras&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![JAX](https://img.shields.io/badge/JAX-000000?style=flat-square&logo=google&logoColor=white)
![vLLM](https://img.shields.io/badge/vLLM-1E88E5?style=flat-square&logo=fastapi&logoColor=white)

### Security & Systems Engineering
![Vulnerability Research](https://img.shields.io/badge/Security-Vulnerability%20Research-red?style=flat-square&logo=target&logoColor=white)
![Code Auditing](https://img.shields.io/badge/Audit-Secure%20Code%20Review-critical?style=flat-square&logo=securityscorecard&logoColor=white)
![Fountain Codes](https://img.shields.io/badge/Algorithm-Fountain%20Codes%20(LT)-blueviolet?style=flat-square)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)

### Backend, Web & Databases
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=flat-square&logo=bootstrap&logoColor=white)

</div>

---

## GitHub Activity

<div align="center">

<p align="center">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmadhanalagarsamy%2Fmadhanalagarsamy%2Fmain%2F.github%2Fbadges%2Fissues-total.json&style=for-the-badge" alt="Total Issues Opened" />
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmadhanalagarsamy%2Fmadhanalagarsamy%2Fmain%2F.github%2Fbadges%2Fissues-open.json&style=for-the-badge" alt="Currently Open" />
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmadhanalagarsamy%2Fmadhanalagarsamy%2Fmain%2F.github%2Fbadges%2Fissues-closed.json&style=for-the-badge" alt="Closed Issues" />
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmadhanalagarsamy%2Fmadhanalagarsamy%2Fmain%2F.github%2Fbadges%2Fprs-total.json&style=for-the-badge" alt="PRs Opened" />
</p>

<!-- START_DYNAMIC_STATS -->
<div align="center">
  <table>
    <tr>
      <td align="center" width="16%"><b>Issues Opened</b><br/><code>18</code></td>
      <td align="center" width="16%"><b>Currently Open</b><br/><code>11</code></td>
      <td align="center" width="16%"><b>Closed Issues</b><br/><code>7</code></td>
      <td align="center" width="16%"><b>PRs Opened</b><br/><code>12</code></td>
      <td align="center" width="16%"><b>Public Repos</b><br/><code>9</code></td>
      <td align="center" width="16%"><b>Followers</b><br/><code>2</code></td>
    </tr>
  </table>
  <p><sub>Live metrics synced with GitHub API &bull; Last updated: 2026-08-28 17:58 UTC</sub></p>
</div>
<!-- END_DYNAMIC_STATS -->

<br/>

<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=madhanalagarsamy&bg_color=0b0d17&color=38bdf8&line=818cf8&point=c084fc&area=true&hide_border=true" width="100%" alt="Contribution Graph" />
</p>

</div>

---

## 🔥 Recent Work

<!-- START_DYNAMIC_PROJECTS -->
| Repository | Description | Primary Tech | Stars | Last Synced |
| :--- | :--- | :---: | :---: | :---: |
| [**`creative-corner-ecommerce`**](https://github.com/madhanalagarsamy/creative-corner-ecommerce) | Production-grade e-commerce backend and SSR platform featuring a 4-tier magic-byte customer file validation pipeline, dynamic lead-time engine, and custom quote builder. | `Python` | ⭐ 0 | 2026-08-26 |
| [**`vllm`**](https://github.com/madhanalagarsamy/vllm) *(upstream fork)* | A high-throughput and memory-efficient inference and serving engine for LLMs | `Python / C++` | ⭐ 1 | 2026-08-19 |
| [**`future-agi`**](https://github.com/madhanalagarsamy/future-agi) *(upstream fork)* | Open-source, end-to-end platform for evaluating, observing, and improving LLM and AI agent applications. Tracing · Evals · Simulations · Datasets · Gateway · Guardrails. Self-hostable. Apache 2.0. | `Python / C++` | ⭐ 0 | 2026-08-18 |
| [**`national-people-database-face-recognition-system`**](https://github.com/madhanalagarsamy/national-people-database-face-recognition-system) | Biometric citizen record management system featuring real-time camera capture, bounding box detection, and dual-engine facial verification. | `Python` | ⭐ 0 | 2026-08-18 |
<!-- END_DYNAMIC_PROJECTS -->

---

## Open Source Contributions

<div align="center">

<p>I actively contribute security audits, bug fixes, and feature implementations across key open-source technologies:</p>

<table align="center">
  <tr>
    <td align="center"><img src="https://img.shields.io/badge/Google-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google" /></td>
    <td align="center"><img src="https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white" alt="Keras" /></td>
    <td align="center"><img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" alt="TensorFlow" /></td>
    <td align="center"><img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" /></td>
  </tr>
  <tr>
    <td align="center"><img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" /></td>
    <td align="center"><img src="https://img.shields.io/badge/Future--AGI-000000?style=for-the-badge&logo=apache&logoColor=white" alt="Future-AGI" /></td>
    <td align="center"><img src="https://img.shields.io/badge/BigBlueButton-2C4376?style=for-the-badge&logo=bigbluebutton&logoColor=white" alt="BigBlueButton" /></td>
    <td align="center"><img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" /></td>
  </tr>
</table>

</div>

---

## Connect With Me

<div align="center">

[![Website](https://img.shields.io/badge/Net%20Corporation-netcorporation.site-0ea5e9?style=for-the-badge&logo=google-chrome&logoColor=white)](https://netcorporation.site)
[![GitHub](https://img.shields.io/badge/GitHub-madhanalagarsamy-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/madhanalagarsamy)

<p>
  Reach out via <b><a href="https://netcorporation.site">netcorporation.site</a></b> for security audits, technical research inquiries, or collaborative engineering initiatives.
</p>

</div>

---

<!--ISSUE_STATS_START-->
<table align="center">
  <tr>
    <td align="center"><b>Total Issues Opened</b><br/>18</td>
    <td align="center"><b>Currently Open</b><br/>11</td>
    <td align="center"><b>Closed</b><br/>7</td>
    <td align="center"><b>PRs Opened</b><br/>12</td>
  </tr>
</table>
<p align="center"><sub>Last updated: 2026-08-28 17:58 UTC</sub></p>
<!--ISSUE_STATS_END-->
