# == Schema Information
#
# Table name: roles
#
#  id         :bigint(8)        not null, primary key
#  role_name  :string(255)      not null
#  created_at :datetime
#  updated_at :datetime
#

FactoryBot.define do
  factory :role do
    sequence(:role_name) { |n| "member-#{n}" }
  end
end
