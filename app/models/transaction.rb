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

# require 'aasm'
class Transaction < ApplicationRecord
  # include AASM

  belongs_to :loan, optional: true
  belongs_to :saving, optional: true
  belongs_to :user

  # after_validation :set_balances

  validates :user_id, :amount, presence: true
  validate :loan_or_saving_present

  after_commit :set_balances, :update_user, on: :create

  # aasm whiny_transitions: false do
  #   state :pending, initial: true
  #   state :confirmed
  #
  #   event :confirm do
  #     transitions from: :pending, to: :confirmed
  #   end
  # end

  private

  def loan_or_saving_present
    return if (loan_id || saving_id).present?
    # TODO: add error
  end

  def set_balances
    self.previous_balance ||= loan.try(:balance) || saving.try(:balance)
    self.new_balance ||= previous_balance - amount
  end

  def update_user
    # loan.present? ? loan.balance = new_balance : saving.balance = new_balance
    # send confrimation of update back to co-op
  end
end
