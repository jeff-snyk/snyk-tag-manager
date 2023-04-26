# Snyk Tag Manager

A simple GUI application to help delete tags for app.snyk.io using the Snyk API.

## Prerequisites

This project requires Python 3, requests and Tkinter.

You'll also need your Snyk Group ID (found in the Group Settings page) and [Snyk API token](https://docs.snyk.io/snyk-admin/snyk-broker/snyk-broker-code-agent/setting-up-the-code-agent-broker-client-deployment/step-1-obtaining-the-required-tokens-for-the-setup-procedure/obtaining-your-snyk-api-token).

### Checking for Tkinter

Tkinter is the standard GUI library for Python and comes pre-installed with most Python installations. You can check if it's installed by running:

```bash
python -m tkinter
```

If Tkinter is installed, a small test window will appear. Close the window to continue.

If Tkinter is not installed, you can try one of the following methods to install it:
#### Using Homebrew (macOS)

Note: This method can take a long time.
```bash
brew install python-tk
```

#### Using pip (not tested, but the internet tells me it works.)
```bash
pip3 install tk
```

### Installing requests
You can install requests either from requirements.txt:
```bash
pip install -r requirements.txt
```

Or just install it:
```bash
pip install requests
```

## Running the Application
1. Clone this repository to your local machine and navigate to the project directory.
```bash
git clone https://github.com/yourusername/snyk-tag-manager.git
cd snyk-tag-manager

```

2. Run the Python script.
```bash
python snyk_tag_manager.py
```

The application will open, and you can use it to manage tags for your Snyk account.

To delete a tag, click  "Delete" next to the tag. If the deletion is successful, the tag will be removed from the list. If an error occurs, an error message will be displayed.

