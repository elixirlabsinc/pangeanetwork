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

class Saving < ApplicationRecord
  belongs_to :user
  has_many :transactions

  validates :user_id, :balance, presence: true
end
