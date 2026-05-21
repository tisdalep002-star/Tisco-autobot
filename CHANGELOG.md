# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-05-21

### Added
- Comprehensive README with features, examples, and troubleshooting
- Development dependencies (black, isort, pylint, pytest)
- `.env.example` template for environment configuration
- Enhanced Makefile with color-coded output and additional targets
- `.gitignore` with Python, IDE, and virtual environment rules
- CHANGELOG.md for version tracking
- Basic documentation structure

### Improved
- Better error handling and user feedback
- Enhanced command structure in Makefile
- More intuitive CLI help messages

### Fixed
- Import organization and code consistency

## [1.0.0] - 2026-02-19

### Initial Release

#### Features
- ✨ Interactive terminal interface powered by Claude AI
- 🔧 Four core tools:
  - Bash execution for system commands
  - File operations (write/append)
  - HTTP requests (REST API calls)
  - Token inspection and analysis
- 🎨 Rich terminal UI with styled output
- 🧠 Autonomous decision-making with tool selection
- 💾 Conversation history management
- 📊 Token usage tracking

#### Tools
- **bash**: Full system access with process management
- **write_file**: Safe file operations with path expansion
- **http_request**: REST API interactions with custom headers
- **inspect_tokens**: Claude model tokenization analysis

#### UI
- Beautiful ASCII art splash screen
- Color-coded output (magenta, cyan, green, yellow, red)
- Real-time streaming responses
- Formatted panels and tables for results
- Tool execution visualization

---

## Roadmap

### [1.2.0] - Planned
- [ ] Configuration profiles (dev, prod, staging)
- [ ] Extended logging capabilities
- [ ] Performance metrics and analytics
- [ ] Custom theme support
- [ ] Session persistence

### [2.0.0] - Planned
- [ ] Multi-model support (switching models)
- [ ] Async execution for long-running tasks
- [ ] Web UI interface
- [ ] API server mode
- [ ] Plugin architecture
- [ ] Advanced memory/context management
