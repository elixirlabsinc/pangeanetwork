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

FactoryBot.define do
  factory :transaction do
    user
    amount { 200 }

    trait :with_loan do
      saving { nil }
      loan
    end

    trait :with_saving do
      loan { nil }
      saving
    end
  end
end
