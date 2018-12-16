require File.expand_path(File.dirname(__FILE__) + '/../test_helper')

class CoOpTest < ActiveSupport::TestCase
  context 'CoOp' do
    context 'valiadations' do
      should validate_presence_of(:name)
      should validate_presence_of(:phase_id)
      should validate_presence_of(:start_date)
      should validate_presence_of(:is_active)
    end
  end
end
