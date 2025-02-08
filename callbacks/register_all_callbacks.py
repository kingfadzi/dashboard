# register_all_callbacks.py
from .filter_callbacks import register_filter_callbacks
from .active_inactive_callbacks import register_active_inactive_callbacks
from .classification_callbacks import register_classification_callbacks
from .contributors_callbacks import register_contributors_callbacks
from .language_callbacks import register_language_callbacks
from .cloc_callbacks import register_cloc_callbacks
from .iac_callbacks import register_iac_callbacks
from .language_contributors_callbacks import register_language_contributors_callbacks
from .vulnerability_callbacks import register_vulnerability_callbacks
from .multi_language_usage_callbacks import register_multi_language_usage_callbacks
from .last_commit_callbacks import register_last_commit_callbacks
from .label_tech_callbacks import register_label_tech_callbacks
from .kpi_callbacks import register_kpi_callbacks

def register_all_callbacks(app):
    register_filter_callbacks(app)
    register_active_inactive_callbacks(app)
    register_classification_callbacks(app)
    register_contributors_callbacks(app)
    register_language_callbacks(app)
    register_cloc_callbacks(app)
    register_iac_callbacks(app)
    register_language_contributors_callbacks(app)
    register_vulnerability_callbacks(app)
    register_multi_language_usage_callbacks(app)
    register_last_commit_callbacks(app)
    register_label_tech_callbacks(app)
    register_kpi_callbacks(app)
    