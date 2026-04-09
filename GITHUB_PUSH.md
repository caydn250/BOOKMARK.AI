# Push NotebookLM to GitHub

Your local Git repository is ready! Follow these steps to create a GitHub repository and push your code.

## 📋 Prerequisites

- GitHub account (free at https://github.com/signup)
- Git installed (already have it!)
- Git authenticated with GitHub

## 🚀 Step-by-Step Guide

### Step 1: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Fill in the repository details:
   - **Repository name**: `NotebookLM`
   - **Description**: `Document QA system with BM25 retrieval - no vector embeddings needed`
   - **Visibility**: Choose `Public` or `Private`
   - **Initialize repo**: Leave blank (don't initialize with README)
3. Click **"Create repository"**

### Step 2: Connect Local Repository to GitHub

After creating the repo, GitHub will show you commands. Run:

```powershell
cd c:\Users\Jayant\Desktop\NotebookLM

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/NotebookLM.git

# Verify remote added
git remote -v
```

You should see:
```
origin  https://github.com/YOUR_USERNAME/NotebookLM.git (fetch)
origin  https://github.com/YOUR_USERNAME/NotebookLM.git (push)
```

### Step 3: Push to GitHub

```powershell
cd c:\Users\Jayant\Desktop\NotebookLM

# Push main branch to GitHub
git branch -M main
git push -u origin main
```

On first push, you may be prompted to authenticate:
- **GitHub will open a browser** for authentication
- OR use a **Personal Access Token** if using HTTPS

### Step 4: Verify Upload

1. Go to `https://github.com/YOUR_USERNAME/NotebookLM`
2. You should see all your files:
   - backend/ folder with Python modules
   - frontend/ folder with HTML/JS
   - Documentation files (README.md, START_HERE.md, etc.)
   - requirements.txt

## ✅ If Pushing with Authentication

### Option A: Personal Access Token (Recommended)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo` (full control of private repositories)
4. Copy the token
5. When git asks for password, paste the token instead

### Option B: SSH Key

1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add to GitHub: https://github.com/settings/keys
3. Use SSH URL: `git@github.com:YOUR_USERNAME/NotebookLM.git`

## 📝 Quick Command Cheatsheet

```powershell
# View current remote
git remote -v

# Add GitHub remote
git remote add origin https://github.com/YOUR_USERNAME/NotebookLM.git

# Change main branch name
git branch -M main

# Push to GitHub
git push -u origin main

# View commit history
git log --oneline

# Check status
git status
```

## 🔄 Future Updates

After initial setup, for future pushes:

```powershell
cd c:\Users\Jayant\Desktop\NotebookLM
git add .
git commit -m "Your commit message"
git push origin main
```

## 📚 Helpful Links

- GitHub Docs: https://docs.github.com/en/repositories
- Git Commands: https://git-scm.com/docs
- SSH Setup: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## 💡 Tips

1. **Naming**: Use `main` (default) instead of `master` for new repos
2. **Commits**: Write clear, descriptive commit messages
3. **.gitignore**: Already configured to exclude .venv, __pycache__, etc.
4. **Branch Strategy**: Start with `main` branch for simplicity
5. **Documentation**: Your README.md will display on GitHub homepage

## 🎯 After Upload

Once uploaded to GitHub, you can:

1. **Share**: Send GitHub link to others
2. **Collaborate**: Add contributors
3. **Deploy**: Use GitHub Actions for CI/CD
4. **Track Issues**: Use GitHub Issues for bug tracking
5. **Release**: Create releases on GitHub
6. **Clone**: `git clone https://github.com/YOUR_USERNAME/NotebookLM.git`

---

**Ready to push? Run the commands in Step 1-3 above!**

Need help? Check GitHub documentation at https://docs.github.com
