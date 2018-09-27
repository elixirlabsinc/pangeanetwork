# == Schema Information
#
# Table name: loans
#
#  id         :bigint(8)        not null, primary key
#  user_id    :integer          not null
#  balance    :integer          not null
#  interest   :integer          not null
#  loan_start :datetime         not null
#  loan_end   :datetime         not null
#  created_at :datetime
#  updated_at :datetime
#

FactoryBot.define do
  factory :loan do
    user
    balance { rand(500) }
    interest { rand(10) }
    loan_start { 2.days.ago }
    loan_end { 2.years.from_now }
  end
end
