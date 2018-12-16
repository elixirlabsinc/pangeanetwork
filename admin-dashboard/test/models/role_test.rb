require File.expand_path(File.dirname(__FILE__) + '/../test_helper')

class RoleTest < ActiveSupport::TestCase
  context 'Role' do
    context 'valiadations' do
      should validate_presence_of(:role_name)
    end
  end
end
