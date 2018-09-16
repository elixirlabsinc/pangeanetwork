# == Schema Information
#
# Table name: savings
#
#  id         :bigint(8)        not null, primary key
#  user_id    :integer          not null
#  balance    :integer          not null
#  created_at :datetime
#  updated_at :datetime
#

FactoryBot.define do
  factory :saving do
    user
    balance { rand(500) }
  end
end
