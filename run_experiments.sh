#!/bin/bash

# List of models to process
models=(
     "/hkfs/work/workspace_haic/scratch/sb7059-llm_models/huggingface/hub/phi-4"
)

# Function to kill vllm server
kill_vllm_server() {
    echo "Killing vLLM server..."
    pkill -9 -f vLLM
    sleep 5  # Wait for server to properly shutdown
}

# Function to check if server is running
check_server() {
    curl -s http://localhost:8086/v1/models >/dev/null
    return $?
}

# Trap Ctrl+C and cleanup
trap kill_vllm_server EXIT
cd /home/iai/sb7059/git/GenAICyberSecMCQA

# Loop through each model
for modelname in "${models[@]}"; do
    echo "Processing model: $modelname"
    
    # Start vLLM server
    echo "Starting vLLM server for $modelname..."
    PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True /home/iai/sb7059/git/vLLM_Test/.venv/bin/python -m vllm.entrypoints.openai.api_server \
        --host 0.0.0.0 \
        --port 8086 \
        --gpu-memory-utilization 1 \
        --enforce-eager \
        --download-dir /hkfs/work/workspace_haic/scratch/sb7059-llm_models/huggingface/hub \
        --model "$modelname" &

    # Wait for server to start with periodic checks
    echo "Waiting for server to initialize..."
    sleep 30

    # Check server availability with timeout
    max_attempts=60  # Maximum number of attempts (60 * 15 seconds = 15 minutes timeout)
    attempt=1
    server_ready=false

    while [ $attempt -le $max_attempts ]; do
        echo "Checking server availability (attempt $attempt/$max_attempts)..."
        
        if check_server; then
            echo "Server is ready!"
            server_ready=true
            break
        else
            echo "Server not ready yet, waiting..."
            sleep 15
            ((attempt++))
        fi
    done

    if [ "$server_ready" = false ]; then
        echo "Server failed to start after $max_attempts attempts. Skipping this model."
        kill_vllm_server
        continue
    fi

    # Run the experiment
    echo "Running experiment for $modelname..."
    .venv/bin/python main.py \
        --config config_ccna_5shot.yaml \
        --model "$modelname"

    echo "Running ccnp"
    .venv/bin/python main.py \
        --config config_ccnp_5shot.yaml \
        --model "$modelname"

    echo "Running mmlu"
    .venv/bin/python main.py \
        --config config_mmlu.yaml \
        --model "$modelname"

    echo "Running ccna cot"
    .venv/bin/python main.py \
        --config config_ccna_COT.yaml \
        --model "$modelname"

    # Kill the vLLM server
    kill_vllm_server

    echo "Completed processing for $modelname"
    echo "----------------------------------------"
done

echo "All models processed successfully!"
