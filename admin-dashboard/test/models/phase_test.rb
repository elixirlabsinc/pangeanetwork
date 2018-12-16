require File.expand_path(File.dirname(__FILE__) + '/../test_helper')

class PhaseTest < ActiveSupport::TestCase
  context 'Phase' do
    context 'valiadations' do
      should validate_presence_of(:phase_type)
    end
  end
end
