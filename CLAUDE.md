# Chessling Academy – Developer & Git Guidelines

## 1. Architecture & Repositories

### A. iOS & macOS App (STRICTLY PRIVATE)
- **Local Directory:** `/Users/tobias/Documents/MacDev/Chessling`
- **Remote Git:** `https://github.com/tas231/Chessling-Academy.git`
- **GitHub Visibility:** `PRIVATE`
- **Purpose:** Confidential Swift codebase, Xcode project, engine algorithms (Titan), didactic lessons, audio models, and tests.
- **Safety Rule:** NEVER publish this code to any public repository or online cloud service. Keep the remote visibility strictly private.
- **Branch:** `main`

### B. App Store Showcase & Legal Website (PUBLIC GITHUB PAGES)
- **Local Directory:** `/Users/tobias/Documents/MacDev/Chessling-Site`
- **Remote Git:** `https://github.com/tas231/Chessling-Site.git`
- **GitHub Visibility:** `PUBLIC` (required for GitHub Pages)
- **Live URL:** `https://tas231.github.io/Chessling-Site/`
- **App Store URLs:**
  - Privacy Policy: `https://tas231.github.io/Chessling-Site/#privacy`
  - Support: `https://tas231.github.io/Chessling-Site/#support`
  - Legal Notice / Impressum: `https://tas231.github.io/Chessling-Site/#imprint`
- **Content:** ONLY `index.html` and the `assets/` folder (images, logos, screenshots).
- **Safety Rule:** NEVER copy or commit Swift code, Xcode project files, or private keys into `Chessling-Site`.

---

## 2. Push & Deployment Commands

### To commit & push App Code updates:
```bash
cd /Users/tobias/Documents/MacDev/Chessling
git add .
git commit -m "Your descriptive message"
git push origin main
```

### To update & deploy the Website:
```bash
# 1. Update index.html / assets in /Users/tobias/Documents/MacDev/Chessling-Site
cd /Users/tobias/Documents/MacDev/Chessling-Site
git add index.html assets/
git commit -m "Update website"
git push origin main
# GitHub Pages deploys automatically within ~30 seconds
```

---

## 3. Technology & Rules
- **Swift / Xcode:** Target macOS 14+ and iOS 17+. Native SwiftUI, zero external tracking, 100% offline capable, Apple "Made for Kids" & COPPA compliant.
- **Website:** Self-contained vanilla HTML5 + embedded CSS + embedded lightweight vanilla JS for the 6-language switcher (DE, EN, ES, FR, TR, ZH). No cookies, no external fonts, GDPR compliant.
