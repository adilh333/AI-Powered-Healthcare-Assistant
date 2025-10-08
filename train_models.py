#!/usr/bin/env python3
"""
Training script for Healthcare Assistant ML models
This script trains all disease prediction models and saves them for deployment
"""

import os
import sys
import argparse
from ml_models import HealthcareMLPipeline
from data_preprocessing import HealthDataPreprocessor

def main():
    parser = argparse.ArgumentParser(description='Train Healthcare Assistant ML models')
    parser.add_argument('--samples', type=int, default=5000, 
                       help='Number of samples to generate (default: 5000)')
    parser.add_argument('--output-dir', type=str, default='models',
                       help='Output directory for trained models (default: models)')
    parser.add_argument('--use-real-data', action='store_true', default=True,
                       help='Use real UCI Heart Disease dataset (default: True)')
    parser.add_argument('--use-synthetic', action='store_true',
                       help='Use synthetic data instead of real dataset')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Healthcare Assistant - ML Model Training")
    print("=" * 60)
    
    # Determine data source
    use_real_data = args.use_real_data and not args.use_synthetic
    if use_real_data:
        print(f"Using UCI Heart Disease Dataset with {args.samples:,} samples...")
    else:
        print(f"Generating {args.samples:,} synthetic health records...")
    
    print(f"Output directory: {args.output_dir}")
    print()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Initialize ML pipeline
        pipeline = HealthcareMLPipeline()
        pipeline.model_path = args.output_dir
        
        # Train all models
        print("Starting model training...")
        results = pipeline.train_all_models(n_samples=args.samples, use_real_data=use_real_data)
        
        print("\n" + "=" * 60)
        print("Training Results Summary")
        print("=" * 60)
        
        # Print results summary
        for disease, models in results.items():
            print(f"\n{disease.replace('_', ' ').title()} Prediction:")
            print("-" * 40)
            for model_name, result in models.items():
                print(f"  {model_name:20} AUC: {result['auc_score']:.4f}")
        
        # Find best models
        print("\n" + "=" * 60)
        print("Best Models Selected")
        print("=" * 60)
        
        for disease, models in results.items():
            best_model = max(models.keys(), key=lambda x: models[x]['auc_score'])
            best_auc = models[best_model]['auc_score']
            print(f"{disease.replace('_', ' ').title():20} {best_model:20} (AUC: {best_auc:.4f})")
        
        print(f"\nModels saved to: {args.output_dir}/")
        print("Training completed successfully!")
        
        # Verify saved models
        print("\nVerifying saved models...")
        saved_models = []
        for disease in ['diabetes', 'heart_disease', 'eye_disease']:
            model_path = f"{args.output_dir}/{disease}_model.pkl"
            if os.path.exists(model_path):
                saved_models.append(disease)
                print(f"  ✓ {disease}_model.pkl")
            else:
                print(f"  ✗ {disease}_model.pkl (missing)")
        
        if len(saved_models) == 3:
            print("\nAll models saved successfully!")
        else:
            print(f"\nWarning: Only {len(saved_models)}/3 models saved successfully")
            sys.exit(1)
            
    except Exception as e:
        print(f"\nError during training: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
