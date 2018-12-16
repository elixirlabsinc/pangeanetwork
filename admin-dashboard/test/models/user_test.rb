require File.expand_path(File.dirname(__FILE__) + '/../test_helper')

class UserTest < ActiveSupport::TestCase
  context 'User' do
    context 'valiadations' do
      should validate_presence_of(:phone)
      should validate_presence_of(:role_id)
      should validate_uniqueness_of(:phone)
    end
  end
end
