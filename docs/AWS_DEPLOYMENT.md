# Deploying to AWS Elastic Beanstalk

This guide details how to deploy the ProctoriaX Testing Platform to AWS Elastic Beanstalk (EB).

## Prerequisites

1.  **AWS Account**: Ensure you have an active AWS account.
2.  **EB CLI**: Install the Elastic Beanstalk Command Line Interface.
    ```bash
    pip install awsebcli --upgrade --user
    ```
    *or on macOS with brew:*
    ```bash
    brew install awsebcli
    ```
3.  **AWS Identity**: Configure your AWS credentials.
    ```bash
    aws configure
    ```

## 1. Initialize Elastic Beanstalk

Navigate to the project root directory:

```bash
cd /path/to/project/testing-platform
```

Initialize the EB application:

```bash
eb init
```
- **Region**: Select your preferred region (e.g., us-east-1).
- **Application Name**: Enter `proctoriax-platform` (or default).
- **Platform**: Select `Python`.
- **Platform Branch**: Select `Python 3.11 running on 64bit Amazon Linux 2023` (or similar).
- **SSH**: Set up SSH if you want to access the instance later.

## 2. Create the Environment

Create a new environment (this will provision EC2, Load Balancer, etc.):

```bash
eb create proctoriax-env
```
This process may take a few minutes.

## 3. Configure Database (RDS)

For production, you should use an RDS database (MySQL).

1.  Go to the [AWS Elastic Beanstalk Console](https://console.aws.amazon.com/elasticbeanstalk).
2.  Select your environment (`proctoriax-env`).
3.  Go to **Configuration** -> **Database**.
4.  Click **Edit**.
5.  **Engine**: `mysql`
6.  **Version**: 8.0.x
7.  **Instance class**: `db.t3.micro` (free tier eligible) or larger.
8.  **Username/Password**: Set a secure username and password.
9.  Click **Apply**.

Once the database is created, Beanstalk passes connection details via environment variables:
- `RDS_HOSTNAME`
- `RDS_PORT`
- `RDS_DB_NAME`
- `RDS_USERNAME`
- `RDS_PASSWORD`

Ensure your application uses these variables. If your app uses a single `DATABASE_URL` or `SQLALCHEMY_DATABASE_URI`, you may need to construct it in the **Software** configuration (see below) or modify your `config.py` to use `RDS_*` variables if present.

## 4. Environment Variables

You must set the `FLASK_ENV` and `SECRET_KEY` variables.

1.  In the EB Console, go to **Configuration** -> **Updates, monitoring, and logging**.
2.  Scroll down to **Environment properties**.
3.  Add the following properties:
    - `FLASK_ENV` = `production`
    - `SECRET_KEY` = `your-super-secure-secret-key-here`
    - `FLASK_APP` = `run.py` (optional, as Procfile handles start)
    
    *If you aren't using the automatic RDS variables in your code code directly, construct the DB URI here:*
    - `SQLALCHEMY_DATABASE_URI` = `mysql+pymysql://USER:PASS@HOST:PORT/DBNAME`

4.  Click **Apply**.

 alternatively, using CLI:
```bash
eb setenv FLASK_ENV=production SECRET_KEY=changeme
```

## 5. Deploy Updates

When you make changes to your code:

1.  Commit your changes to git.
2.  Deploy:
    ```bash
    eb deploy
    ```

## 6. Open the Application

To check if the application is running:

```bash
eb open
```

## Troubleshooting

- **Logs**: To verify errors, check the logs.
    ```bash
    eb logs
    ```
- **502 Bad Gateway**: Check `eb logs`. Usually means Gunicorn failed to start.
- **Static files not loading**: Ensure `.ebextensions/01-flask.config` exists and is correct.
