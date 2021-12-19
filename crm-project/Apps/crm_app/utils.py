
# dict for manual standard sorting in ClientListView
headers = {
    'title': 'asc',
    'date_created': 'asc',
}

# for filters InterplaysFilter
SORT_CHOICES_InterplaysFilter = (
        ('client_acs', 'client acs'),
        ('client_desc', 'client desc'),
        ('project_acs', 'project acs'),
        ('project_desc', 'project desc'),
        ('created_acs', 'created acs'),
        ('created_desc', 'created desc'),
)

# for filters ClientsInfoFilter
SORT_CHOICES_ClientsInfoFilter = (
        ('title_acs', 'title acs'),
        ('title_desc', 'title desc'),
        ('created_acs', 'created acs'),
        ('created_desc', 'created desc'),
    )

# for model InterPlaysList
link_status_InterPlaysListModel = (
    ('cl', 'by claim'),
    ('le', 'by letter'),
    ('si', 'by site'),
    ('co', 'by company'),
)
