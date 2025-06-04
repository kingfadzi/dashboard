from .build_info_callbacks import register_build_info_callbacks
from .code_insights_callbacks import register_code_insights_callbacks
from .code_insights_cloc import register_code_insights_cloc_callbacks
from .code_insights_gitlog_callbacks import register_code_insights_gitlog_callbacks
from .code_insights_lizard_callbacks import register_code_insights_lizard_callbacks
from .dependencies_callbacks import register_dependencies_callbacks
from .dropdown_callbacks import register_dropdown_callbacks
from .overview_callbacks import register_overview_callbacks
from .register_filter_callbacks import register_filter_callbacks
from .register_filter_value_callbacks import register_filter_value_callbacks
from .repo_profile_callback import register_repo_profile_callbacks
from .table_callbacks import register_table_callbacks
from .kpi_callbacks import register_kpi_callbacks
from .dependency_insights import register_dependency_insights_callbacks


def register_all_callbacks(app):
    register_filter_callbacks(app)
    register_code_insights_callbacks(app)
    register_code_insights_gitlog_callbacks(app)
    register_code_insights_cloc_callbacks(app)
    register_code_insights_lizard_callbacks(app)
    register_build_info_callbacks(app)
    register_dependencies_callbacks(app)
    register_table_callbacks(app)
    #register_filter_value_callbacks(app)
    register_kpi_callbacks(app)
    register_overview_callbacks(app)
    register_repo_profile_callbacks(app)
    register_dependency_insights_callbacks(app)
    register_dropdown_callbacks(app)
