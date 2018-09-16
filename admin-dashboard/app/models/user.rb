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

class User < ApplicationRecord
  belongs_to :role
  belongs_to :co_op
  has_one :saving
  has_one :loan

  validates :phone, :role_id, presence: true
  validates :phone, uniqueness: true
end
