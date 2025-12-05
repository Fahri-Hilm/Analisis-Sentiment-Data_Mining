"""
Model Versioning and Experiment Tracking
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any
import pickle

class ModelVersionManager:
    """Manage model versions and experiments"""
    
    def __init__(self, version_dir: str = "data/models/versions"):
        self.version_dir = Path(version_dir)
        self.version_dir.mkdir(parents=True, exist_ok=True)
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
    
    def save_version(self, model, feature_extractor, label_encoder,
                    metrics: Dict[str, Any], config: Dict[str, Any],
                    version_name: str = None) -> str:
        """Save model version with metadata"""
        if version_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            version_name = f"v_{timestamp}"
        
        version_path = self.version_dir / version_name
        version_path.mkdir(parents=True, exist_ok=True)
        
        # Save model
        with open(version_path / "model.pkl", 'wb') as f:
            pickle.dump(model, f)
        
        # Save feature extractor
        with open(version_path / "feature_extractor.pkl", 'wb') as f:
            pickle.dump(feature_extractor, f)
        
        # Save label encoder
        with open(version_path / "label_encoder.pkl", 'wb') as f:
            pickle.dump(label_encoder, f)
        
        # Save metadata
        metadata = {
            'version_name': version_name,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'config': config
        }
        
        with open(version_path / "metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Model version saved: {version_name}")
        return str(version_path)
    
    def load_version(self, version_name: str):
        """Load model version"""
        version_path = self.version_dir / version_name
        
        if not version_path.exists():
            raise ValueError(f"Version {version_name} not found")
        
        with open(version_path / "model.pkl", 'rb') as f:
            model = pickle.load(f)
        
        with open(version_path / "feature_extractor.pkl", 'rb') as f:
            feature_extractor = pickle.load(f)
        
        with open(version_path / "label_encoder.pkl", 'rb') as f:
            label_encoder = pickle.load(f)
        
        with open(version_path / "metadata.json", 'r') as f:
            metadata = json.load(f)
        
        self.logger.info(f"Model version loaded: {version_name}")
        return model, feature_extractor, label_encoder, metadata
    
    def list_versions(self) -> list:
        """List all saved versions"""
        versions = []
        for version_dir in sorted(self.version_dir.iterdir()):
            if version_dir.is_dir():
                metadata_path = version_dir / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    versions.append({
                        'name': version_dir.name,
                        'timestamp': metadata.get('timestamp'),
                        'metrics': metadata.get('metrics', {})
                    })
        return versions
    
    def get_best_version(self, metric: str = 'accuracy') -> Dict[str, Any]:
        """Get best version by metric"""
        versions = self.list_versions()
        
        if not versions:
            raise ValueError("No versions found")
        
        best_version = max(
            versions,
            key=lambda v: v['metrics'].get(metric, 0)
        )
        
        return best_version
