# BH Arithmetic

A first version of a small web calculator. Enter two numbers, choose addition, subtraction, multiplication, or division, and the Python server returns the result to the page.

## Run it on Windows

You need Python 3.9 or newer. No packages need to be installed.

1. Open this project folder in VS Code.
2. Open the integrated terminal in this folder.
3. Start the server:

   ```powershell
   py app.py
   ```

4. Open <http://127.0.0.1:8000> in your browser.
5. Stop the server with `Ctrl+C` in the terminal.

Python does the arithmetic in `app.py`; the browser files in `index.html`, `styles.css`, and `app.js` provide the page and send the choices to Python. Division by zero and invalid numbers show a clear error instead of a result.

## Build a standalone Windows app

The standalone build is a single executable that includes Python and the web page files. It opens the calculator in your default browser and does not require Python to be installed on the computer running the executable.

1. Open PowerShell in this project folder.
2. Run the build script:

   ```powershell
   .\build_standalone.ps1
   ```

3. When the build finishes, double-click `dist\BH_Arithmetic.exe`. A console window stays open while the calculator is running; close it or press `Ctrl+C` to stop the app.

The build script creates a project-local `.venv` and installs PyInstaller there. The generated executable is in `dist`; rebuild it after changing the source files. This first version is unsigned, so Windows may display a security warning when the executable is copied to another computer.

## Run the tests

From the project folder, run:

```powershell
py -m unittest discover -s tests -v
```

## GitHub setup for Bruno and Victoria

Use two separate GitHub accounts, one for Bruno Heusser and one for Victoria Heusser. Each person should keep their own sign-in and use their own Git identity; do not share passwords or access tokens. The account that owns the repository can add the other person as a collaborator.

### Create and publish the repository

1. Sign in to GitHub as the intended repository owner and create a new repository named `BH_Software_Projekt_1`.
2. Choose **Private** if this is personal or unfinished work; choose **Public** only if both collaborators are comfortable publishing the code. Do not initialize it with a README, `.gitignore`, or license because this project already has local files.
3. In a terminal opened in this project folder, initialize Git and make the first commit:

   ```powershell
   git init
   git add .
   git commit -m "Initial arithmetic calculator"
   git branch -M main
   git remote add origin https://github.com/YOUR_GITHUB_OWNER/BH_Software_Projekt_1.git
   git push -u origin main
   ```

   Replace `YOUR_GITHUB_OWNER` with the repository owner's GitHub username. GitHub will prompt you to authenticate; use Git Credential Manager or SSH rather than putting a token in a command.
4. On GitHub, open **Settings > Collaborators** (the exact menu label may vary), choose **Add people**, and invite the other person's GitHub username. They must accept the invitation.
5. Each collaborator sets their own author name and email on their computer. Use the email associated with their GitHub account, or a GitHub-provided private `noreply` email:

   ```powershell
   git config --global user.name "Bruno Heusser"
   git config --global user.email "YOUR_GITHUB_EMAIL"
   ```

   Victoria runs the same commands with her own name and email on her computer. These settings label commits; repository access is controlled separately by GitHub.

### A simple collaboration routine

- Keep `main` in a working state. Make each change on a short branch such as `feature/add-keyboard-support` or `fix/decimal-rounding`.
- Commit small, descriptive changes, for example `Add division-by-zero validation`.
- Push the branch and open a pull request into `main`. The other collaborator reviews it, checks the tests, and approves before it is merged.
- Before starting another change, update the local `main` branch with `git pull`.
- Never commit passwords, tokens, or private data. `.gitignore` excludes Python cache files and common local environment folders.

### Start a change on a branch

```powershell
git switch main
git pull
git switch -c feature/your-change
```

When the change is ready, run the tests, commit it, push the branch, and open a pull request on GitHub:

```powershell
   py -m unittest discover -s tests -v
git add .
git commit -m "Describe the change"
git push -u origin feature/your-change
```

## Next improvements

This is intentionally a small starting point. Good next steps include adding browser-level tests, improving decimal precision requirements, code-signing the Windows executable, and adding a GitHub Actions workflow to run the unit tests for every pull request.