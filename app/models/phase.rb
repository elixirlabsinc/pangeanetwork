# == Schema Information
#
# Table name: phases
#
#  id         :bigint(8)        not null, primary key
#  phase_type :string(255)
#  created_at :datetime
#  updated_at :datetime
#

class Phase < ApplicationRecord
  validates :phase_type, presence: true
end
