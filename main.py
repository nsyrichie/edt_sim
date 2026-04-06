#!/usr/bin/env python3
"""
Main entry point for the simulation framework.
"""

import argparse
import sys
import logging
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from simulation.core import Simulation
from utils.logging_setup import setup_logging

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run simulation")
    parser.add_argument(
        "--config", 
        type=str, 
        default="configs/simulation.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["train", "eval", "visualize"],
        default="train",
        help="Running mode"
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default=None,
        help="Path to checkpoint for evaluation"
    )
    parser.add_argument(
        "--device",
        type=str,
        choices=["cpu", "cuda"],
        default="cuda",
        help="Device to run on"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()

def main():
    """Main execution function."""
    args = parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting simulation framework")
    logger.info(f"Mode: {args.mode}")
    logger.info(f"Device: {args.device}")
    
    try:
        # Initialize simulation
        sim = Simulation(args.config, device=args.device)
        
        if args.mode == "train":
            logger.info("Starting training mode")
            from agents.trainer import Trainer
            trainer = Trainer(sim, args.config)
            trainer.train()
            
        elif args.mode == "eval":
            logger.info("Starting evaluation mode")
            if args.checkpoint:
                sim.load_checkpoint(args.checkpoint)
            results = sim.evaluate(num_episodes=10)
            logger.info(f"Evaluation results: {results}")
            
        elif args.mode == "visualize":
            logger.info("Starting visualization mode")
            sim.visualize()
            
        logger.info("Simulation completed successfully")
        
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())