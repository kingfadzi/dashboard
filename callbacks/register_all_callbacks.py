from .build_info_callbacks import register_build_info_callbacks
from .code_insights_callbacks import register_code_insights_callbacks
from .code_insights_cloc import register_code_insights_cloc_callbacks
from .code_insights_gitlog_callbacks import register_code_insights_gitlog_callbacks
from .code_insights_lizard_callbacks import register_code_insights_lizard_callbacks
from .dependencies_callbacks import register_dependencies_callbacks
from .register_filter_callbacks import register_filter_callbacks
from .active_inactive_callbacks import register_active_inactive_callbacks
from .classification_callbacks import register_classification_callbacks
from .contributors_callbacks import register_contributors_callbacks
from .language_callbacks import register_language_callbacks
from .cloc_callbacks import register_cloc_callbacks
from .iac_callbacks import register_iac_callbacks
from .language_contributors_callbacks import register_language_contributors_callbacks
from .register_filter_value_callbacks import register_filter_value_callbacks
from .vulnerability_callbacks import register_vulnerability_callbacks
from .multi_language_usage_callbacks import register_multi_language_usage_callbacks
from .last_commit_callbacks import register_last_commit_callbacks
from .kpi_callbacks import register_kpi_callbacks
from .appserver_callbacks import register_appserver_callbacks
from .dev_frameworks_callbacks import register_dev_frameworks_callbacks
from .dependency_types_callbacks import register_dependency_types_callbacks
from .switch_view_callbacks import register_switch_view_callbacks

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
    register_kpi_callbacks(app)
    register_appserver_callbacks(app)
    register_dev_frameworks_callbacks(app)
    register_dependency_types_callbacks(app)
    register_switch_view_callbacks(app)
    register_code_insights_callbacks(app)
    register_code_insights_gitlog_callbacks(app)
    register_code_insights_cloc_callbacks(app)
    register_code_insights_lizard_callbacks(app)
    register_build_info_callbacks(app)
    register_dependencies_callbacks(app)
    register_filter_value_callbacks(app)
