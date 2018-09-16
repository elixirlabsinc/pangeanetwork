# == Schema Information
#
# Table name: users
#
#  id                 :bigint(8)        not null, primary key
#  email              :string(255)
#  encrypted_password :string(255)
#  role_id            :integer
#  created_at         :datetime
#  updated_at         :datetime
#  co_op_id           :integer
#  first_name         :string(255)
#  last_name          :string(255)
#  phone              :string(255)      not null
#

FactoryBot.define do
  factory :user do
    co_op
    sequence(:email) { |n| "test#{n}@test.com" }
    # password { 'password' }
    # password_confirmation 'password'
    role
    sequence(:phone) { |n| "111-#{n}" }
    first_name { 'Jane' }
    last_name { 'Doe' }
  end
end
