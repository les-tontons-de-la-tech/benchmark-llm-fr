#!/bin/bash
# Run complet : les 14 modèles de texte OVH non encore testés, 120 tâches chacun, en parallèle.
set -u
cd /root/work/benchmark-llm-fr || exit 1
export BENCH_API_KEY="$OVH_AI_ENDPOINTS_API_KEY"
BASE="https://oai.endpoints.kepler.ai.cloud.ovh.net/v1"

declare -A M=(
  [DeepSeek-V4.1-Flash-1017]=deepseek_v41_flash
  [gemma-4-26b-a4b]=gemma_4_26b
  [gpt-oss-120b]=gptoss_120b
  [gpt-oss-20b]=gptoss_20b
  [laguna-xs-2.1]=laguna_xs
  [Meta-Llama-3_3-70B-Instruct]=llama33_70b
  [nemotron3-nano-30b]=nemotron_nano
  [nemotron3-omni-30b]=nemotron_omni
  [Qwen2.5-VL-72B-Instruct]=qwen25vl_72b
  [Qwen3.5-397B-A17B]=qwen35_397b
  [Qwen3.6-27B]=qwen36_27b
  [Qwen3.8-27B]=qwen38_27b
  [qwen3-vl-30b-a3b]=qwen3vl_30b
  [qwen3.6-35b-a3b]=qwen36_35b_a3b
)

for model in "${!M[@]}"; do
  slug="${M[$model]}"
  python3 scripts/runner.py --model "$model" --base-url "$BASE" \
    --max-tokens 8000 --temperature 0.8 \
    --out "runs/${slug}.jsonl" > "logs_${slug}.txt" 2>&1 &
  sleep 1
done
wait
echo "run complet terminé"
