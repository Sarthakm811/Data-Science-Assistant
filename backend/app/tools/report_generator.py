"""Report Generator - Create PDF and notebook reports"""
from typing import Dict, Any
from pathlib import Path
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir: str = "/outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_markdown_report(self, analysis_results: Dict[str, Any], job_id: str) -> str:
        """Generate markdown report"""
        report = []
        report.append(f"# Data Science Analysis Report")
        report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Job ID:** {job_id}\n")
        
        # Dataset info
        if 'basic_info' in analysis_results:
            info = analysis_results['basic_info']
            report.append("## Dataset Overview")
            report.append(f"- **Rows:** {info['shape'][0]}")
            report.append(f"- **Columns:** {info['shape'][1]}")
            report.append(f"- **Memory:** {info['memory_usage_mb']:.2f} MB\n")
        
        # Summary statistics
        if 'summary_stats' in analysis_results:
            report.append("## Summary Statistics")
            report.append("Key statistical measures for numeric features.\n")
        
        # Missing data
        if 'missing_data' in analysis_results:
            missing = analysis_results['missing_data']
            if missing['total_missing'] > 0:
                report.append("## Missing Data Analysis")
                report.append(f"Total missing values: {missing['total_missing']}\n")
        
        # ML Results
        if 'ml_results' in analysis_results:
            ml = analysis_results['ml_results']
            report.append("## Machine Learning Results")
            report.append(f"**Task Type:** {ml['task_type']}")
            report.append(f"**Best Model:** {ml['best_model']}\n")
        
        # Insights
        if 'insights' in analysis_results:
            report.append("## AI-Generated Insights")
            report.append(analysis_results['insights'])
        
        report_text = "\n".join(report)
        
        # Save report
        report_path = self.output_dir / f"{job_id}_report.md"
        report_path.write_text(report_text)
        
        return str(report_path)
    
    def generate_notebook(self, code: str, job_id: str) -> str:
        """Generate Jupyter notebook"""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# Data Science Analysis\n", f"Job ID: {job_id}"]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": code.split('\n')
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        notebook_path = self.output_dir / f"{job_id}_analysis.ipynb"
        with open(notebook_path, 'w') as f:
            json.dump(notebook, f, indent=2)
        
        return str(notebook_path)
