//
//  FriendsTableCell.m
//  puuten
//
//  Created by wang jialei on 12-8-14.
//
//

#import "FriendsTableCell.h"
#import "UIImageView+WebCache.h"

@implementation FriendsTableCell

- (id)initWithStyle:(UITableViewCellStyle)style reuseIdentifier:(NSString *)reuseIdentifier
{
    self = [super initWithStyle:style reuseIdentifier:reuseIdentifier];
    if (self) {
        nameLbl = [[UILabel alloc] initWithFrame:CGRectZero];
        [[self contentView] addSubview:nameLbl];
        //[nameLbl release];
        
        avatar = [[UIImageView alloc] initWithFrame:CGRectZero];
        [[self contentView] addSubview:avatar];
        
        checked = [[UIButton alloc]initWithFrame:CGRectZero];
        [[self contentView] addSubview:checked];
    }
    return self;
}

- (void)layoutSubviews
{
    [super layoutSubviews];
    nameLbl.frame = CGRectMake(80.0, 5.0, 80.0, 20.0);
    nameLbl.font = [UIFont fontWithName:@"" size:18];
    nameLbl.textColor = [UIColor redColor];
    
    avatar.frame = CGRectMake(5, 5, 40, 40);
    if (!justForShow) {
        checked.frame = CGRectMake( 180, 5, 16, 16);
        [checked setBackgroundImage:[UIImage imageNamed:@"com_btn_check.png"] forState:UIControlStateNormal];
        [checked setBackgroundImage:[UIImage imageNamed:@"com_btn_checked.png"] forState:UIControlStateSelected];
        [checked addTarget:self action:(@selector(chooseBox:)) forControlEvents:UIControlEventTouchUpInside];
    }
}

- (void)chooseBox:(id)sender
{
    if(isChecked){
        ((UIButton *)sender).selected = YES;
        isChecked = NO;
    }
    else{
        ((UIButton *)sender).selected = NO;
        isChecked = YES;
    }
}


- (void)setValue:(NSString *)name avatar:(NSString *)image_url justForShow:(BOOL)just_for_show
{
    [nameLbl setText:name];
    NSURL *avatar_url = [[NSURL alloc] initWithString:image_url];
    [avatar setImageWithURL:avatar_url];
    justForShow = just_for_show;
}

- (void)setSelected:(BOOL)selected animated:(BOOL)animated
{
    [super setSelected:selected animated:animated];

    // Configure the view for the selected state
}

@end
