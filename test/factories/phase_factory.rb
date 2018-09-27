# == Schema Information
#
# Table name: phases
#
#  id         :bigint(8)        not null, primary key
#  phase_type :string(255)
#  created_at :datetime
#  updated_at :datetime
#

FactoryBot.define do
  factory :phase do
    phase_type { 'established' }
  end
end
