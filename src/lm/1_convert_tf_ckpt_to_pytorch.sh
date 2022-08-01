export ALBERT_BASE_DIR=${1}

transformers-cli convert --model_type albert \
  --tf_checkpoint $ALBERT_BASE_DIR/model.ckpt-15000 \
  --config $ALBERT_BASE_DIR/albert_config.json \
  --pytorch_dump_output $ALBERT_BASE_DIR/albert_pytorch_model.bin
