def register_kpi_callbacks(app):
    @app.callback(
        [
            Output("kpi-total-repos", "children"),
            Output("kpi-total-repos-subtext", "children"),

            Output("kpi-avg-commits", "children"),
            Output("kpi-avg-commits-subtext", "children"),

            Output("kpi-avg-contributors", "children"),
            Output("kpi-avg-contributors-subtext", "children"),

            Output("kpi-avg-loc", "children"),
            Output("kpi-avg-loc-subtext", "children"),

            Output("kpi-branches", "children"),
            Output("kpi-branches-subtext", "children"),

            Output("kpi-build-tools", "children"),
            Output("kpi-build-tools-subtext", "children"),

            Output("kpi-runtime", "children"),
            Output("kpi-runtime-subtext", "children"),

            Output("kpi-cicd", "children"),
            Output("kpi-cicd-subtext", "children"),

            Output("kpi-iac", "children"),
            Output("kpi-iac-subtext", "children"),

            Output("kpi-sources", "children"),
            Output("kpi-sources-subtext", "children"),
        ],
        [Input("default-filter-store", "data")],
    )
    def update_kpi_values(store_data):
        filters = extract_filter_dict_from_store(store_data)
        kpi = fetch_overview_kpis(filters)

        # Repo status
        total_repos = kpi.get("total_repos", 0)
        active = kpi.get("active", 0)
        inactive = kpi.get("inactive", 0)

        # Recent activity
        recently_updated = kpi.get("recently_updated", 0)
        new_repos = kpi.get("new_repos", 0)

        # Contributors
        solo = kpi.get("solo_contributor", 0)
        total_contribs = kpi.get("total_contributors", 0)

        # Code metrics
        loc = kpi.get("loc", 0)
        source_files = kpi.get("source_files", 0)

        # Branching
        branch_sprawl = kpi.get("branch_sprawl", 0)

        # Build tools
        build_detected = kpi.get("build_tool_detected", 0)
        modules = kpi.get("modules", 0)
        without_tool = kpi.get("without_tool", 0)

        # Runtime
        runtime_detected = kpi.get("runtime_detected", 0)
        languages = kpi.get("languages", 0)

        # CI/CD
        cicd_total = kpi.get("cicd_total", 0)
        gl = kpi.get("gitlab_ci", 0)
        jenkins = kpi.get("jenkins", 0)

        # IaC
        iac_total = kpi.get("iac_total", 0)
        dockerfile = kpi.get("dockerfile", 0)
        docker_compose = kpi.get("docker_compose", 0)
        helm_charts = kpi.get("helm_charts", 0)

        # Sources
        sources_total = kpi.get("sources_total", 0)
        from_bitbucket = kpi.get("from_bitbucket", 0)
        from_gitlab = kpi.get("from_gitlab", 0)

        return (
            # Total repos
            format_with_commas(total_repos),
            f"Active: {format_number_si(active)} · Inactive: {format_number_si(inactive)}",

            # Commits (recent update + new)
            format_with_commas(recently_updated),
            f"New: {format_number_si(new_repos)} · 30d",

            # Contributors
            format_with_commas(solo),
            f"All: {format_number_si(total_contribs)}",

            # Code size
            format_number_si(loc),
            f"Files: {format_number_si(source_files)} · Repos: {format_number_si(total_repos)}",

            # Branches
            format_with_commas(branch_sprawl),
            ">10 branches",

            # Build tools
            format_with_commas(build_detected),
            f"Modules: {format_number_si(modules)} · NoTool: {format_number_si(without_tool)}",

            # Runtime
            format_with_commas(runtime_detected),
            f"Languages: {format_number_si(languages)}",

            # CI/CD
            format_with_commas(cicd_total),
            f"GitLab: {format_number_si(gl)} · Jenkins: {format_number_si(jenkins)}",

            # IaC
            format_with_commas(iac_total),
            f"Dockerfile: {format_number_si(dockerfile)} · Compose: {format_number_si(docker_compose)} · Helm: {format_number_si(helm_charts)}",

            # Sources
            format_with_commas(sources_total),
            f"Bitbucket: {format_number_si(from_bitbucket)} · GitLab: {format_number_si(from_gitlab)}",
        )