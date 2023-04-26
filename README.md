# Snyk Tag Manager

A simple GUI application to help delete tags for app.snyk.io using the Snyk API.

## Prerequisites

To use this application, you'll need your Snyk Group ID (found in the Group Settings page) and [Snyk API token](https://docs.snyk.io/snyk-admin/snyk-broker/snyk-broker-code-agent/setting-up-the-code-agent-broker-client-deployment/step-1-obtaining-the-required-tokens-for-the-setup-procedure/obtaining-your-snyk-api-token).

## Running the Application
1. Clone this repository to your local machine and navigate to the project directory.
```bash
https://github.com/jeff-snyk/snyk-tag-manager.git
```

2. Move to the project directory.
```bash
cd snyk-tag-manager
```

3. Set up a virtual environment.
```bash
python3 -m venv venv
```

4. Activate the virtual environment.
```bash
source venv/bin/activate
```

5. Install requirements
```bash
pip install -r requirements.txt
```

6. Run the Python script.
```bash
python snyk_tag_manager.py
```

The application will open, and you can use it to manage tags for your Snyk account.

To delete a tag, click  "Delete" next to the tag. If the deletion is successful, the tag will be removed from the list. If an error occurs, an error message will be displayed.  If the tag is used in one or more projects, it will not be deleted.

