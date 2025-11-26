#!/usr/bin/env python3
"""
Script to split CoNLL-U files from raw/diachron into train/dev/test splits.
Randomly distributes sentences across files with 80/10/10 split.
"""

import os
import random
import glob
from pathlib import Path


def read_conllu_sentences(file_path):
    """
    Read all sentences from a CoNLL-U file.
    
    Returns a list of sentences, where each sentence is a list of lines
    (including comments and token data).
    """
    sentences = []
    current_sentence = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            
            if line == '':  # Empty line indicates end of sentence
                if current_sentence:
                    sentences.append(current_sentence)
                    current_sentence = []
            else:
                current_sentence.append(line)
    
    # Add the last sentence if file doesn't end with empty line
    if current_sentence:
        sentences.append(current_sentence)
    
    return sentences


def write_conllu_sentences(sentences, output_path):
    """
    Write sentences to a CoNLL-U file.
    
    Args:
        sentences: List of sentences (each sentence is a list of lines)
        output_path: Path to output file
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, sentence in enumerate(sentences):
            # Write all lines of the sentence
            for line in sentence:
                f.write(line + '\n')
            
            # Add empty line after each sentence (except the last one)
            if i < len(sentences) - 1:
                f.write('\n')


def main():
    # Set up paths
    input_dir = Path('raw/diachron')
    output_dir = Path('.')
    
    # Get all .conllu files
    conllu_files = list(input_dir.glob('*.conllu'))
    
    if not conllu_files:
        print(f"No .conllu files found in {input_dir}")
        return
    
    print(f"Found {len(conllu_files)} CoNLL-U files in {input_dir}")
    
    # Read all sentences from all files
    all_sentences = []
    total_files_processed = 0
    
    for file_path in conllu_files:
        print(f"Reading {file_path.name}...")
        sentences = read_conllu_sentences(file_path)
        all_sentences.extend(sentences)
        total_files_processed += 1
        print(f"  Found {len(sentences)} sentences")
    
    print(f"\nTotal sentences collected: {len(all_sentences)}")
    print(f"Files processed: {total_files_processed}")
    
    # Shuffle sentences randomly
    random.seed(42)  # For reproducible results
    random.shuffle(all_sentences)
    
    # Calculate split sizes
    total_sentences = len(all_sentences)
    train_size = int(0.8 * total_sentences)
    dev_size = int(0.1 * total_sentences)
    test_size = total_sentences - train_size - dev_size
    
    print(f"\nSplit sizes:")
    print(f"  Train: {train_size} sentences ({train_size/total_sentences:.1%})")
    print(f"  Dev:   {dev_size} sentences ({dev_size/total_sentences:.1%})")
    print(f"  Test:  {test_size} sentences ({test_size/total_sentences:.1%})")
    
    # Split the data
    train_sentences = all_sentences[:train_size]
    dev_sentences = all_sentences[train_size:train_size + dev_size]
    test_sentences = all_sentences[train_size + dev_size:]
    
    # Write output files
    output_files = [
        (train_sentences, 'diachron-ud-train.conllu'),
        (dev_sentences, 'diachron-ud-dev.conllu'),
        (test_sentences, 'diachron-ud-test.conllu')
    ]
    
    for sentences, filename in output_files:
        output_path = output_dir / filename
        print(f"\nWriting {len(sentences)} sentences to {output_path}")
        write_conllu_sentences(sentences, output_path)
    
    print("\nDone! Successfully created train/dev/test splits.")
    
    # Verify the files were created
    for _, filename in output_files:
        output_path = output_dir / filename
        if output_path.exists():
            print(f"✓ {filename}: {output_path.stat().st_size} bytes")
        else:
            print(f"✗ {filename}: File not created!")


if __name__ == '__main__':
    main()