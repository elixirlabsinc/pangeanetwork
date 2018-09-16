# == Schema Information
#
# Table name: co_ops
#
#  id                 :bigint(8)        not null, primary key
#  phase_id           :integer          not null
#  is_active          :boolean          not null
#  name               :string(255)      not null
#  start_date         :datetime
#  end_date           :datetime
#  location           :string(255)
#  interest           :integer
#  initial_balance    :integer
#  expected_repayment :integer
#  current_balance    :integer
#

FactoryBot.define do
  factory :co_op do
    phase
    sequence(:name) { |n| "Co-Op #{n}" }
    is_active { true }
  end
end
