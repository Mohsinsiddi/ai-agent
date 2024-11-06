# Autonomous Blockchain-Agents

This repository contains an autonomous agent system built in Python. Agents are designed to communicate and handle tasks such as message processing and token transfers. The code is organized for scalability and includes modules for behaviors, message handling, and utilities.

## Prerequisites

1. **Python 3**: Ensure Python 3 is installed.
2. **Poetry**: Ensure Poetry is installed to manage dependencies. You can install it via:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Mohsinsiddi/ai-agent.git
   cd ai-agent
   ```

2. **Install Dependencies**:
   Use Poetry to install all required dependencies:

   ```bash
   poetry install
   ```

3. **Activate Virtual Environment**:

   - Run the following command to enter Poetry's virtual environment:
     ```bash
     poetry shell
     ```
   - **Why this is necessary**: Running `poetry shell` ensures that your terminal is using the correct virtual environment for this project, isolating dependencies. This step is crucial before initializing or running the project, as it ensures the installed packages are accessible and prevents conflicts with system-wide Python packages.

4. **Environment Setup**:

   - Create a `.env` file from the `.env.example` file:
     ```bash
     cp .env.example .env
     ```
   - Populate `.env` with required values:

     - `WEB3_PROVIDER_URL`: URL of the Web3 provider (e.g., Infura).
     - `TOKEN_ADDRESS`: ERC20 token address for balance checks and transfers.
     - `WALLET1_ADDRESS`: Source wallet 1 address for token transfers. (Note: **Can be same as well**).
     - `WALLET2_ADDRESS`: Source wallet 2 address for token transfers. (Note: **Can be same as well**).
     - `TARGET_ADDRESS`: Target wallet address for token transfers. (Note: **This wallet address will recieve transferred tokens**).
     - `PRIVATE_KEY1`: Private key of the wallet 1 for agent1 (Note: **never commit this to version control**).
     - `PRIVATE_KEY2`: Private key of the wallet 2 for agent2(Note: **never commit this to version control**).

   - **Important**: Ensure `.env` is in `.gitignore` to keep sensitive information safe.

## Running the Project

To start the autonomous agents, ensure you are in the Poetry shell, then run:

```bash
python -m autonomous_agents.main
```
<img width="1175" alt="Screenshot 2024-11-06 at 6 50 55 PM" src="https://github.com/user-attachments/assets/abfab27e-dbf7-4ffa-ad11-20b7857f6a4a">

## Running Tests

- **Basic Test**: Run all tests with:
  ```bash
  poetry run pytest tests/test_autonomous_agents.py -v
  ```
- **With CLI Logs**: For more detailed logs in the CLI, run:
  ```bash
  poetry run pytest tests/test_autonomous_agents.py -v --log-cli-level=DEBUG
  ```

## Code Overview

### Folder Structure

- **core/**: Contains core functionality of the agents, such as agent setup, message boxes, and utilities.
- **handlers/**: Houses message handlers for processing specific message types, such as text or transaction-related messages.
- **behaviors/**: Holds behaviors that define agent actions. For instance, balance checks and random message generation behaviors.
- **utils/**: Contains utility functions and configurations, including logging setup.

### Key Components

- **Handlers**:

  - `MessageHandler`: Abstract base class for handling messages.
  - `HelloMessageHandler`: Processes "hello" messages and logs the receipt.
  - `CryptoTransferHandler`: Manages token transfers between wallets with error handling for balance and transaction issues.

- **Behaviors**:
  - `RandomMessageBehavior`: Periodically generates random messages for agent interaction.
  - `TokenBalanceCheckBehavior`: Checks token balances at set intervals, with detailed logging for each check.

### Logging

- Uses **colorlog** for colorful, structured logs. Configured to display log levels and timestamps for easy debugging.

### Error Handling

- Handlers and behaviors include robust error handling, especially in areas prone to failures like Web3 transactions and balance checks.

<img width="1190" alt="Screenshot 2024-11-06 at 6 53 41 PM" src="https://github.com/user-attachments/assets/b2f19d82-091d-436f-a129-15af2e7a38ed">

## Dependencies

This project relies on the following packages, as specified in `pyproject.toml`:

- **web3** (`^7.4.0`): For interaction with the Ethereum blockchain.
- **eth-typing** (`^5.0.1`): Provides type definitions for Ethereum-related data.
- **eth-account** (`^0.13.4`): Allows for account and private key handling.
- **colorlog** (`^6.9.0`): Adds colorized logging support for better visibility of log levels.
- **python-dotenv** (`^1.0.1`): Loads environment variables from a `.env` file for sensitive configurations.

### Development Dependencies

For testing, the following development dependencies are used:

- **pytest** (`^8.3.3`): Framework for running tests.
- **pytest-asyncio** (`^0.24.0`): Adds asyncio support to pytest for asynchronous tests.
- **pytest-mock** (`^3.14.0`): Provides mock functionality for testing.
