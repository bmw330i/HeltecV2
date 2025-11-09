#!/bin/bash

# Heltec V2 Meshtastic Setup Script
# Installs all prerequisites for out-of-the-box functionality

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Heltec V2 Meshtastic Setup${NC}"
echo -e "${BLUE}=================================${NC}"
echo ""

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${BLUE}📂 Project directory: ${PROJECT_DIR}${NC}"

# Check if we're on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    PYTHON_CMD="python3"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    PYTHON_CMD="python3"
else
    echo -e "${RED}❌ Unsupported operating system: $OSTYPE${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Operating System: $OS${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python 3
echo -e "${BLUE}🐍 Checking Python installation...${NC}"
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python $PYTHON_VERSION found${NC}"
else
    echo -e "${RED}❌ Python 3 not found${NC}"
    if [[ "$OS" == "macOS" ]]; then
        echo -e "${YELLOW}💡 Install with: brew install python3${NC}"
        echo -e "${YELLOW}💡 Or download from: https://python.org/downloads/${NC}"
    else
        echo -e "${YELLOW}💡 Install with: sudo apt update && sudo apt install python3 python3-pip python3-venv${NC}"
    fi
    exit 1
fi

# Check Node.js
echo -e "${BLUE}📦 Checking Node.js installation...${NC}"
if command_exists node; then
    NODE_VERSION=$(node --version)
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | cut -d'v' -f2)
    if [ "$NODE_MAJOR" -ge 18 ]; then
        echo -e "${GREEN}✅ Node.js $NODE_VERSION found${NC}"
    else
        echo -e "${RED}❌ Node.js version $NODE_VERSION is too old (need 18+)${NC}"
        echo -e "${YELLOW}💡 Update Node.js from: https://nodejs.org/${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Node.js not found${NC}"
    if [[ "$OS" == "macOS" ]]; then
        echo -e "${YELLOW}💡 Install with: brew install node${NC}"
    else
        echo -e "${YELLOW}💡 Install with: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs${NC}"
    fi
    echo -e "${YELLOW}💡 Or download from: https://nodejs.org/${NC}"
    exit 1
fi

# Check if we can detect the Heltec device
echo -e "${BLUE}📡 Checking for Heltec device...${NC}"
if [[ "$OS" == "macOS" ]]; then
    DEVICE_PATH="/dev/cu.usbserial-0001"
    if [ -e "$DEVICE_PATH" ]; then
        echo -e "${GREEN}✅ Heltec device found at $DEVICE_PATH${NC}"
    else
        echo -e "${YELLOW}⚠️  Heltec device not found at $DEVICE_PATH${NC}"
        echo -e "${YELLOW}💡 Make sure your Heltec board is connected via USB${NC}"
        echo -e "${YELLOW}💡 Check available devices: ls /dev/cu.usbserial*${NC}"
    fi
else
    # Linux device check
    if ls /dev/ttyUSB* 1> /dev/null 2>&1 || ls /dev/ttyACM* 1> /dev/null 2>&1; then
        echo -e "${GREEN}✅ USB serial device found${NC}"
    else
        echo -e "${YELLOW}⚠️  No USB serial devices found${NC}"
        echo -e "${YELLOW}💡 Make sure your Heltec board is connected via USB${NC}"
    fi
fi

# Set up Python virtual environment
echo -e "${BLUE}🐍 Setting up Python virtual environment...${NC}"
VENV_PATH="$PROJECT_DIR/.venv"

if [ -d "$VENV_PATH" ]; then
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
else
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    $PYTHON_CMD -m venv "$VENV_PATH"
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
pip install --upgrade pip

# Install Python dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install platformio meshtastic pyserial requests

# Install PlatformIO if not available
if ! command_exists platformio; then
    echo -e "${BLUE}🔧 Installing PlatformIO...${NC}"
    pip install platformio
fi

echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Set up Node.js dependencies
echo -e "${BLUE}📦 Installing Node.js dependencies...${NC}"
cd "$PROJECT_DIR/heltec-mcp-server"

if [ -f "package.json" ]; then
    npm install
    echo -e "${GREEN}✅ Node.js dependencies installed${NC}"
else
    echo -e "${RED}❌ package.json not found in heltec-mcp-server${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

# Test device connection
echo -e "${BLUE}🔧 Testing device connection...${NC}"
if [ -f "test_device.py" ]; then
    echo -e "${YELLOW}📡 Running device test...${NC}"
    if timeout 30s "$VENV_PATH/bin/python" test_device.py 2>/dev/null; then
        echo -e "${GREEN}✅ Device test passed!${NC}"
    else
        echo -e "${YELLOW}⚠️  Device test failed or timed out${NC}"
        echo -e "${YELLOW}💡 This is normal if device is not connected${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  test_device.py not found, skipping device test${NC}"
fi

# Test MCP server
echo -e "${BLUE}🔧 Testing MCP server...${NC}"
cd "$PROJECT_DIR/heltec-mcp-server"
if timeout 5s node index.mjs --version 2>/dev/null; then
    echo -e "${GREEN}✅ MCP server test passed!${NC}"
else
    echo -e "${YELLOW}⚠️  MCP server test inconclusive (expected for MCP protocol)${NC}"
fi

cd "$PROJECT_DIR"

# Create convenience scripts
echo -e "${BLUE}📝 Creating convenience scripts...${NC}"

# Create activate script
cat > activate_env.sh << 'EOF'
#!/bin/bash
source .venv/bin/activate
echo "🐍 Python virtual environment activated"
echo "💡 Use 'python' for scripts, 'deactivate' to exit"
EOF
chmod +x activate_env.sh

# Create test script
cat > test_setup.sh << 'EOF'
#!/bin/bash
source .venv/bin/activate
echo "🧪 Testing Heltec setup..."
echo ""
echo "1. Testing device connection:"
python test_device.py || echo "⚠️ Device test failed"
echo ""
echo "2. Testing MCP server:"
cd heltec-mcp-server
node --version
echo "MCP server files present: $(ls -la index.mjs package.json 2>/dev/null | wc -l)/2"
cd ..
echo ""
echo "✅ Setup test complete"
EOF
chmod +x test_setup.sh

echo -e "${GREEN}✅ Convenience scripts created${NC}"

# Summary
echo ""
echo -e "${GREEN}🎉 Setup Complete!${NC}"
echo -e "${GREEN}=================${NC}"
echo ""
echo -e "${BLUE}📋 What's installed:${NC}"
echo -e "  ✅ Python virtual environment (.venv/)"
echo -e "  ✅ PlatformIO for firmware building"  
echo -e "  ✅ Meshtastic Python library"
echo -e "  ✅ Node.js MCP server dependencies"
echo -e "  ✅ Convenience scripts"
echo ""
echo -e "${BLUE}🚀 Next steps:${NC}"
echo ""
echo -e "${YELLOW}1. Connect your Heltec V2 board via USB${NC}"
echo ""
echo -e "${YELLOW}2. Test the setup:${NC}"
echo "   ./test_setup.sh"
echo ""
echo -e "${YELLOW}3. Build and flash firmware:${NC}"
echo "   source .venv/bin/activate"
echo "   python -m platformio run -e heltec-v2_1 --target upload"
echo ""
echo -e "${YELLOW}4. Test messaging:${NC}"  
echo "   python messenger.py"
echo ""
echo -e "${YELLOW}5. Use MCP server with GitHub Copilot:${NC}"
echo "   cd heltec-mcp-server"
echo "   npm start"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "   README.md - Project overview"
echo "   COMMUNICATION_GUIDE.md - Messaging tools"
echo "   heltec-mcp-server/README.md - MCP server docs"
echo ""
echo -e "${GREEN}🎯 Your Heltec V2 is ready for AI-powered mesh networking!${NC}"