# Autonomous Agents Project

This repository contains an autonomous agent system built in Python. Agents are designed to communicate and handle tasks such as message processing and token transfers. The code is organized for scalability, and includes modules for behaviors, message handling, and utilities.

## Prerequisites

1. **Poetry**: Ensure Poetry is installed to manage dependencies. You can install it via:
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

3. **Environment Setup**:

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

To start the autonomous agents, run:

```bash
python -m autonomous_agents.main
```

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
