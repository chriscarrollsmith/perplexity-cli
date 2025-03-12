# Perplexity CLI

Perplexity CLI is a command-line interface for interacting with the Perplexity API. This CLI tool uses the [Click](https://click.palletsprojects.com/) library for building commands.

## Installation

You can install Perplexity CLI directly from the GitHub repository:

```bash
python pip install git+https://github.com/chriscarrollsmith/perplexity-cli.git
```

If you are installing on a system where you don't have administrative privileges, you can install the tool in your user environment with the `--user` flag:

```bash
python pip install --user git+https://github.com/chriscarrollsmith/perplexity-cli.git
```

After a user installation, make sure that your local binary directory is in your PATH. For example, add the following line to your shell configuration file (e.g. `.bashrc` or `.zshrc`):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Configuration

The tool requires an API key to interact with the Perplexity API. You can provide the API key using the `--api-key` option or by setting it as an environment variable:

```bash
export PERPLEXITY_API_KEY="your_api_key_here"
```

To permanently set the API key, add the above command to your `.bashrc` or `.zshrc` file:

```bash
echo "export PERPLEXITY_API_KEY='your_api_key_here'" >> ~/.bashrc
```

## Usage

Run the CLI by providing a query and desired options:

```bash
perplexity "Your query here" [options]
```

### Options

- `-v, --verbose` &ndash; Enable debug mode.
- `-u, --usage` &ndash; Show usage details.
- `-c, --citations` &ndash; Show citations.
- `-g, --glow` &ndash; Enable glow display mode.
- `-a, --api-key` &ndash; Specify the API key directly.
- `-m, --model` &ndash; Select the model to use (default is `sonar-pro`).  
  **Available models:** `sonar-reasoning-pro`, `sonar-reasoning`, `sonar-pro`, `sonar`.

## Example

```bash
perplexity "What is the capital of France?" -v -c -u -m sonar-pro
```

## Repository

For the latest updates, to file issues, or to contribute, please visit the GitHub repository at:  
[https://github.com/chriscarrollsmith/perplexity-cli](https://github.com/chriscarrollsmith/perplexity-cli)
```

### Explanation

- **Installation Section:** Updated to instruct users to install directly from the GitHub repository.
- **Repository Link:** Added a link to the GitHub repo for quick access to source code and further updates.
- **Usage and Options:** Provided clear instructions on how to run the CLI along with a full list of options available.
