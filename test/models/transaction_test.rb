# == Schema Information
#
# Table name: transactions
#
#  id               :bigint(8)        not null, primary key
#  loan_id          :integer
#  saving_id        :integer
#  amount           :integer          not null
#  previous_balance :integer
#  new_balance      :integer
#  user_id          :integer          not null
#  created_at       :datetime
#  updated_at       :datetime
#  aasm_state       :string(255)
#

require File.expand_path(File.dirname(__FILE__) + '/../test_helper')

class TransactionTest < ActiveSupport::TestCase
  context 'Transaction' do
    context 'valiadations' do
      setup do
        create(:transaction, :with_loan)
      end

      should validate_presence_of(:user_id)
      should validate_presence_of(:amount)
    end

    context 'set_balances' do
      context 'paying back a loan' do
        setup do
          @user = create(:user, loan: create(:loan, balance: 500))
          @transaction = build(:transaction, amount: 200, loan: @user.loan, user: @user)
        end

        should 'set previous_balance' do
          @transaction.save

          assert_equal @transaction.previous_balance, @user.loan.balance
        end

        should 'set new_balance' do
          @transaction.save

          assert_equal @transaction.new_balance, (@user.loan.balance - @transaction.amount)
        end
      end

      context 'withdrawing from savings' do
        setup do
          @user = create(:user, saving: create(:saving, balance: 500))
          @transaction = build(:transaction, amount: 200, saving: @user.saving, user: @user)
        end

        should 'set previous_balance' do
          @transaction.save

          assert_equal @transaction.previous_balance, @user.saving.balance
        end

        should 'set new_balance' do
          @transaction.save

          assert_equal @transaction.new_balance, (@user.saving.balance - @transaction.amount)
        end
      end
    end
  end
end
