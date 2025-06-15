from pages.layout_filters import register_filter_tags_callbacks
from callbacks.buildtools.build_info_callbacks import register_build_info_callbacks
from callbacks.codeinsights.code_insights_callbacks import register_code_insights_callbacks
from callbacks.codeinsights.code_insights_cloc import register_code_insights_cloc_callbacks
from callbacks.codeinsights.code_insights_gitlog_callbacks import register_code_insights_gitlog_callbacks
from callbacks.codeinsights.code_insights_lizard_callbacks import register_code_insights_lizard_callbacks
from callbacks.dependencies.dependencies_callbacks import register_dependencies_callbacks
from callbacks.overview.overview_callbacks import register_overview_callbacks
from .repo_profile_callback import register_repo_profile_callbacks
from .shared_modal_callbacks import register_modal_callbacks
from .table_callbacks import register_table_callbacks
from callbacks.overview.kpi_callbacks import register_kpi_callbacks
from callbacks.dependencies.dependency_insights import register_dependency_insights_callbacks


def register_all_callbacks(app):
    #register_filter_callbacks(app)
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
    #register_dropdown_callbacks(app)

    register_filter_tags_callbacks(app)

    register_modal_callbacks(app)

