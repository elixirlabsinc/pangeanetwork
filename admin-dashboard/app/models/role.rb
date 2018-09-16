# == Schema Information
#
# Table name: roles
#
#  id         :bigint(8)        not null, primary key
#  role_name  :string(255)      not null
#  created_at :datetime
#  updated_at :datetime
#

class Role < ApplicationRecord
  has_many :users

  validates :role_name, presence: true, uniqueness: true
end
