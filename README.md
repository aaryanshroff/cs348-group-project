# CS 348 Group Project

## Prerequisites

Ensure you have the following installed:

- Python 3.11+
- pip
- Node.js (v22+)
- npm

## Setup

1. Clone the Repository

   ```bash
   git clone https://github.com/aaryanshroff/cs348-group-project
   cd cs348-group-project
   ```

2. Run the Setup Script

    ```bash
    # MacOS / Linux
    ./scripts/bash/setup.sh
    ```

    ```powershell
    # Windows
    .\scripts\powershell\setup.ps1
    ```

## Running the Application

### Backend
Open a new terminal and run:
```bash
# MacOS / Linux
./scripts/bash/run_backend.sh
```

```powershell
# Windows
.\scripts\powershell\run_backend.ps1
```

### Frontend
Open a new terminal and run:
```bash
# MacOS / Linux
./scripts/bash/run_frontend.sh
```

```powershell
# Windows
.\scripts\powershell\run_frontend.ps1
```

## Supported Features

### Basic Features

- **R7 - List all restaurants**


## Milestones

### Milestone 1
How to build and test sample DB:
```bash
cd backend/databases
sqlite3 sample_dataset.db < ../sql/create_tables.sql
python3 sample_db_files/populate_sample_db.py
sqlite3 sample_dataset.db < ../sql/test-sample.sql > ../sql/test-sample.out
```