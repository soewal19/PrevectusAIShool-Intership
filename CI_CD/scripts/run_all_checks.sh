
#!/bin/bash

# Run all quality checks
echo "Starting all quality checks..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &amp;&amp; pwd )"

# Run linting
"$SCRIPT_DIR/run_linting.sh"
if [ $? -ne 0 ]; then
    echo "Linting failed!"
    exit 1
fi

# Run type checking
"$SCRIPT_DIR/run_typecheck.sh"
if [ $? -ne 0 ]; then
    echo "Type checking failed!"
    exit 1
fi

# Run tests
"$SCRIPT_DIR/run_tests.sh"
if [ $? -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi

echo "All checks passed! 🎉"

