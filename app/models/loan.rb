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

class Loan < ApplicationRecord
  belongs_to :user
  has_many :transactions

  validates :user_id, :balance, :loan_start, :loan_end, :interest, presence: true
end
