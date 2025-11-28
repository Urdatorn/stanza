
# första test

Jag har 90/10 train/dev på hela den historiska maskinparsade korpusen alanev52/Diachronic_Treebanks_DigPhil/stanza_results plus alla fem svenska trädbanker från ud

test är vårt guld, alanev52/Diachronic_Treebanks_DigPhil/stanza_results/validated

tmux attach -t stanza

jag kör med:

python -m stanza.utils.datasets.prepare_depparse_treebank UD_Swedish-diachronic --wordvec_pretrain_file /Users/albin/stanza_resources/sv/pretrain/diachronic.ft

python -m stanza.utils.training.run_depparse UD_Swedish-diachronic --batch_size 32 --dropout 0.33
