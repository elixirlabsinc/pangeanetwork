admin_role = Role.find_or_create_by!(role_name: 'admin')
officer_role = Role.find_or_create_by!(role_name: 'officer')
member_role = Role.find_or_create_by!(role_name: 'member')
