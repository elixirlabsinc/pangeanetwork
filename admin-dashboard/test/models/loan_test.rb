require File.expand_path(File.dirname(__FILE__) + '/../test_helper')

class LoanTest < ActiveSupport::TestCase
  context 'Loan' do
    context 'valiadations' do
      setup do
        create(:loan)
      end
      should validate_presence_of(:user_id)
      should validate_presence_of(:balance)
      should validate_presence_of(:loan_start)
      should validate_presence_of(:loan_end)
      should validate_presence_of(:interest)
    end
  end
end
